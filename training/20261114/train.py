from pathlib import Path
import argparse,json,math,time,hashlib,os
os.environ.setdefault('HF_HUB_OFFLINE','1');os.environ.setdefault('TOKENIZERS_PARALLELISM','false')
import torch
from datasets import Dataset
from transformers import AutoTokenizer,TrainerCallback,set_seed
from peft import LoraConfig
from trl import SFTConfig,SFTTrainer
ROOT=Path(__file__).resolve().parents[1]
class CheckFinite(TrainerCallback):
 def on_log(self,args,state,control,logs=None,**kwargs):
  for k,v in (logs or {}).items():
   if isinstance(v,(float,int)) and not math.isfinite(v):raise RuntimeError(f'Nonfinite metric {k}')
  (ROOT/'audit/progress.json').write_text(json.dumps({'global_step':state.global_step,'max_steps':state.max_steps,'epoch':state.epoch,'logs':logs,'updated_at':time.time()},indent=2))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--smoke',action='store_true');a=ap.parse_args()
 c=json.loads((ROOT/'configs/qlora.json').read_text());manifest=json.loads((ROOT/'audit/model_manifest.json').read_text());assert manifest['revision']==c['base_revision']
 set_seed(c['seed']);tok=AutoTokenizer.from_pretrained(c['model_path'],local_files_only=True)
 if tok.pad_token_id is None:tok.pad_token=tok.eos_token
 data={};length_audit={}
 for split in ['train','validation']:
  with (ROOT/'data'/f'{split}.jsonl').open() as f:rows=[json.loads(line) for line in f]
  accepted=[];dropped=[]
  for r in rows:
   ids=tok.apply_chat_template(r['prompt']+r['completion'],tokenize=True)
   if len(ids)>c['max_length']:dropped.append({'sample_id':r['sample_id'],'tokens':len(ids)});continue
   accepted.append({'prompt':r['prompt'],'completion':r['completion']})
  length_audit[split]={'accepted':len(accepted),'excluded_over_length':dropped}
  if a.smoke:accepted=accepted[:4 if split=='train' else 2]
  elif split=='validation':accepted=accepted[:64]
  assert accepted;data[split]=Dataset.from_list(accepted)
 (ROOT/'audit/token_length_audit.json').write_text(json.dumps(length_audit,indent=2))
 output=ROOT/('smoke_output' if a.smoke else 'output');assert not (output/'adapter_final').exists(),'Refusing to overwrite a completed adapter'
 args=SFTConfig(output_dir=str(output),max_length=c['max_length'],per_device_train_batch_size=1,per_device_eval_batch_size=1,gradient_accumulation_steps=1 if a.smoke else c['gradient_accumulation_steps'],learning_rate=c['learning_rate'],num_train_epochs=c['epochs'],max_steps=2 if a.smoke else -1,bf16=True,gradient_checkpointing=True,gradient_checkpointing_kwargs={'use_reentrant':False},optim='adamw_torch',lr_scheduler_type='cosine',warmup_steps=0 if a.smoke else 10,max_grad_norm=1.0,logging_steps=1,logging_nan_inf_filter=False,eval_strategy='no',save_strategy='no' if a.smoke else 'steps',save_steps=50,save_total_limit=2,report_to='none',seed=c['seed'],packing=False,completion_only_loss=True,assistant_only_loss=False,prediction_loss_only=True,dataloader_pin_memory=False,model_init_kwargs={'device_map':{'':0},'dtype':torch.bfloat16,'attn_implementation':'sdpa','local_files_only':True},use_cache=False)
 peft=LoraConfig(r=c['lora_rank'],lora_alpha=c['lora_alpha'],lora_dropout=c['lora_dropout'],target_modules=c['target_modules'],bias='none',task_type='CAUSAL_LM')
 trainer=SFTTrainer(model=c['model_path'],args=args,train_dataset=data['train'],eval_dataset=data['validation'],processing_class=tok,peft_config=peft,callbacks=[CheckFinite()])
 # Check completion masking actually leaves supervised labels and masks prompt tokens.
 batch=next(iter(trainer.get_train_dataloader()));assert (batch['labels']!=-100).any();assert (batch['labels']==-100).any()
 trainable=sum(p.numel() for p in trainer.model.parameters() if p.requires_grad);assert 0<trainable<1_000_000_000
 baseline=trainer.evaluate();result=trainer.train();final=trainer.evaluate();trainer.save_model(str(output/'adapter_final'));tok.save_pretrained(output/'adapter_final')
 adapter_config=output/'adapter_final/adapter_config.json'
 cfg=json.loads(adapter_config.read_text());cfg['base_model_name_or_path']=c['base_repository'];cfg['revision']=c['base_revision'];adapter_config.write_text(json.dumps(cfg,indent=2))
 for p in trainer.model.parameters():
  if p.requires_grad:assert torch.isfinite(p).all(),'Nonfinite adapter weights'
 metrics={'phase':'smoke' if a.smoke else 'formal','trainable_parameters':trainable,'baseline_validation':baseline,'training':result.metrics,'final_validation':final,'peak_gpu_allocated_bytes':torch.cuda.max_memory_allocated(),'peak_gpu_reserved_bytes':torch.cuda.max_memory_reserved(),'base_repository':c['base_repository'],'base_revision':c['base_revision'],'validation_examples_scored':len(data['validation']),'clinical_validation_performed':False}
 (output/'metrics.json').write_text(json.dumps(metrics,indent=2));print('TRAINING_COMPLETE',json.dumps(metrics),flush=True)
if __name__=='__main__':main()
