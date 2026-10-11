import copy
import hashlib
import json
from pathlib import Path
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from neuropanel.backend import MockBackend, HTTPBackend
from neuropanel.pipeline import Pipeline, validate_config
from neuropanel.retrieval import retrieve
from neuropanel.schema import diagnosis_output
from neuropanel.voting import aggregate

ROOT = Path(__file__).resolve().parents[1]

class ReferenceTests(unittest.TestCase):
    def setUp(self):
        self.c = json.loads((ROOT/'configs/reference.demo.json').read_text())
        self.case = json.loads((ROOT/'examples/reference_case.json').read_text())
        self.bank = json.loads((ROOT/'examples/reference_bank.json').read_text())

    def pipeline(self, backend=None):
        return Pipeline(self.c, backend or MockBackend(), ROOT/'prompts/reference')

    def test_full_trace_and_bounded_refinement(self):
        p = self.pipeline();result = p.run(self.case, self.bank)
        self.assertEqual(result['selected_diagnosis'], 'candidate a')
        self.assertEqual(result['call_count'], 8)
        self.assertTrue(result['unresolved_critic_issues'])
        self.assertEqual(p.trace['status'], 'complete')
        self.assertEqual(len(p.trace['retrieved']), 1)
        self.assertTrue(all('raw_response' in c for c in p.trace['calls']))

    def test_single_disables_other_stages(self):
        self.c['mode'] = 'single'
        p = self.pipeline();r = p.run(self.case)
        self.assertEqual(r['call_count'], 1)
        self.assertEqual(p.trace['retrieved'], [])
        self.assertEqual(p.trace['agents'][0]['reviews'], [])

    def test_critic_pass_stops_refinement(self):
        class Passing(MockBackend):
            def complete(self, messages, settings, stage):
                r = super().complete(messages, settings, stage)
                if stage == 'critique':
                    r['choices'][0]['message']['content'] = json.dumps({'coverage':[1]*4,'contradiction_penalty':0,'major_issue':False,'feedback':'No fixture issue'})
                return r
        self.assertEqual(self.pipeline(Passing()).run(self.case,self.bank)['call_count'],4)

    def test_truncation_fails_and_retains_raw(self):
        class Truncated(MockBackend):
            def complete(self,*a):
                r=super().complete(*a);r['choices'][0]['finish_reason']='length';return r
        p=self.pipeline(Truncated())
        with self.assertRaises(ValueError):p.run(self.case,self.bank)
        self.assertEqual(p.trace['status'],'failed')
        self.assertEqual(p.trace['calls'][0]['raw_response']['choices'][0]['finish_reason'],'length')

    def test_invalid_json_fails(self):
        class Invalid(MockBackend):
            def complete(self,*a):
                r=super().complete(*a);r['choices'][0]['message']['content']='not json';return r
        p=self.pipeline(Invalid())
        with self.assertRaises(ValueError):p.run(self.case,self.bank)
        self.assertEqual(len(p.trace['calls']),1)

    def test_retrieval_exclusions(self):
        same=copy.deepcopy(self.bank[0]);same['case_id']=self.case['case_id']
        duplicate=copy.deepcopy(self.bank[0]);duplicate['case_id']='OTHER';duplicate['case_text']=self.case['case_text'].upper()
        self.assertEqual(retrieve(self.case,[same,duplicate],self.c['retrieval']),[])
        self.case['patient_id']='P1';self.bank[0]['patient_id']='P1'
        self.assertEqual(retrieve(self.case,self.bank,self.c['retrieval']),[])

    def test_frozen_embedding_identity_and_dimensions(self):
        self.bank[0]['embedding_revision']='other'
        with self.assertRaises(ValueError):retrieve(self.case,self.bank,self.c['retrieval'])
        self.bank[0]['embedding_revision']='synthetic-vectors-v1';self.bank[0]['embedding']=[1,0,0]
        with self.assertRaises(ValueError):retrieve(self.case,self.bank,self.c['retrieval'])

    def test_ranked_cosine_retrieval(self):
        second=copy.deepcopy(self.bank[0]);second.update(case_id='DEMO-002',embedding=[0,1])
        r=retrieve(self.case,[second,self.bank[0]],self.c['retrieval'])
        self.assertEqual(r[0]['case_id'],'DEMO-001')

    def test_voting_duplicate_alias_missing_and_tie(self):
        def output(items):return {'differential_diagnosis':[{'diagnosis':d,'score':s} for d,s in items]}
        v={'top_k':1,'soft_weight':0.5,'aliases':{'Alpha':'A'}}
        r=aggregate([output([('Alpha',0.8),('A',0.7)]),output([('B',0.8)])],v)
        self.assertEqual(r['selected_diagnosis'],'a')
        self.assertEqual(r['ranking'][0]['hard_votes'],1)
        self.assertAlmostEqual(r['ranking'][0]['mean_self_reported_score'],0.4)
        self.assertAlmostEqual(r['ranking'][0]['vote_score'],1.4)

    def test_invalid_score_and_configuration(self):
        with self.assertRaises(ValueError):diagnosis_output({'symptom_analysis':'','further_tests':'','final_conclusion':'','differential_diagnosis':[{'diagnosis':'A','score':float('nan')}]})
        self.c['agents'][1]['id']=self.c['agents'][0]['id']
        with self.assertRaises(ValueError):validate_config(self.c)

    def test_http_request_contract(self):
        received=[]
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def do_POST(self):
                received.append((self.path,json.loads(self.rfile.read(int(self.headers['Content-Length'])))))
                body=json.dumps({'choices':[{'message':{'content':'{}'},'finish_reason':'stop'}]}).encode()
                self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(body)
        server=HTTPServer(('127.0.0.1',0),Handler)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            cfg={**self.c['backend'],'base_url':f'http://127.0.0.1:{server.server_port}/v1','model':'fixture'}
            response=HTTPBackend(cfg).complete([{'role':'user','content':'synthetic'}],{'max_tokens':8},'generate')
            self.assertEqual(received[0][0],'/v1/chat/completions')
            self.assertEqual(received[0][1]['model'],'fixture')
            self.assertEqual(response['_transport_attempts'][0]['status'],'ok')
        finally:server.shutdown();server.server_close();thread.join()

if __name__=='__main__':unittest.main()
