from pathlib import Path
import json,re,hashlib,collections
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
BASE=Path(__file__).resolve().parents[3];ROOT=Path(__file__).resolve().parents[1]
def read(p):
 with p.open() as f:return [json.loads(l) for l in f]
def norm(s):return re.sub(r'\W+','',s.casefold())
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
rows=read(BASE/'neuro_training_data/20261114_expansion/processed/combined_neuro_candidates.jsonl')
clinical=[]
for p in [BASE/'revision_work/gpt_oss_group2/input_manifest.jsonl',BASE/'revision_work/deepseek_spark_deployment/experiment_protocol/input_manifest.jsonl']:
 if p.exists():clinical+=read(p)
ctext=list({norm(r['case_text']) for r in clinical})
questions=[norm(r['question']) for r in rows]
# Character TF-IDF finds near-verbatim duplicates; it is not a semantic/cross-language detector.
v=TfidfVectorizer(analyzer='char',ngram_range=(3,5),min_df=2,max_features=150000,dtype=np.float32)
X=v.fit_transform(questions+ctext);n=len(rows)
parent=list(range(n))
def find(i):
 while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
 return i
def union(i,j):
 a,b=find(i),find(j)
 if a!=b:parent[max(a,b)]=min(a,b)
nn=NearestNeighbors(metric='cosine',algorithm='brute',radius=.10,n_jobs=2).fit(X[:n])
near_pairs=0
for start in range(0,n,256):
 distances,indices=nn.radius_neighbors(X[start:start+256])
 for off,ids in enumerate(indices):
  for j in ids:
   if j>start+off:union(start+off,int(j));near_pairs+=1
excluded=set();clinical_max=0.0
if ctext:
 nc=NearestNeighbors(metric='cosine',n_neighbors=1,algorithm='brute',n_jobs=2).fit(X[n:]);dist,_=nc.kneighbors(X[:n]);clinical_max=float(1-dist.min());excluded={i for i,d in enumerate(dist[:,0]) if d<=.20 or questions[i] in set(ctext)}
for i in list(excluded):excluded.update(j for j in range(n) if find(j)==find(i))
groups=collections.defaultdict(list)
for i,r in enumerate(rows):
 if i not in excluded:groups[find(i)].append(i)
sets={'train':[],'validation':[]};membership=[]
for group,ids in groups.items():
 groupkey=min(sha(questions[i]) for i in ids); split='validation' if int(groupkey[:8],16)%10==0 else 'train'
 for i in ids:
  r=rows[i];q=r['question'];options=r.get('options')
  if options:q+='\n\n'+'\n'.join(f'{chr(65+k)}. {o}' for k,o in enumerate(options))
  instruction='请根据提供的医学问题作答；病例诊断题给出最可能诊断，信息不足时明确说明。' if r.get('language')=='zh' else 'Answer the medical question using the supplied findings. For diagnostic cases, give the most likely diagnosis and acknowledge insufficient information when applicable.'
  sets[split].append({'prompt':[{'role':'user','content':instruction+'\n\n'+q}],'completion':[{'role':'assistant','content':r['answer']}],'sample_id':r['id'],'source':r['source'],'group_id':groupkey,'language':r.get('language','en')})
  membership.append({'sample_id':r['id'],'question_sha256':sha(questions[i]),'split':split,'group_id':groupkey,'source':r['source']})
for split,data in sets.items():
 with (ROOT/'data'/f'{split}.jsonl').open('w') as f:
  for r in data:f.write(json.dumps(r,ensure_ascii=False)+'\n')
(ROOT/'audit/split_membership.json').write_text(json.dumps(membership,indent=2))
audit={'input_candidates':n,'train':len(sets['train']),'validation':len(sets['validation']),'near_duplicate_pairs':near_pairs,'group_count':len(groups),'local_clinical_unique_cases_checked':len(ctext),'clinical_overlap_excluded':len(excluded),'highest_clinical_character_similarity':clinical_max,'train_validation_group_overlap':len({r['group_id'] for r in sets['train']}&{r['group_id'] for r in sets['validation']}),'clinical_review':'public dataset labels; not independently clinician-adjudicated','third_batch_included':False,'overlap_method':'normalized exact match plus char 3-5gram TF-IDF, clinical cosine>=0.8, public duplicate cosine>=0.9; semantic/bilingual leakage not ruled out','files':{s:hashlib.sha256((ROOT/'data'/f'{s}.jsonl').read_bytes()).hexdigest() for s in sets}}
assert audit['train_validation_group_overlap']==0
(ROOT/'audit/data_preparation.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2));print(json.dumps(audit,ensure_ascii=False,indent=2))
