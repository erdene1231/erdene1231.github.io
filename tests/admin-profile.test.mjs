import test from'node:test';import assert from'node:assert/strict';import {validateAdminProfileChanges,saveAdminProfile}from'../admin-profile.js';
const p={user_id:'00000000-0000-0000-0000-000000000002',snapshot:'a'.repeat(32),username:'student'},values={first_name:' New ',last_name:' Name ',username:'NEW_student'};
test('admin profile client limits fields and sends stable target/snapshot without Auth calls',async()=>{
 assert.deepEqual(validateAdminProfileChanges(values,p),{first_name:'New',last_name:'Name',username:'new_student'});
 for(const k of ['email','school','avatar_path','password','role','progress'])assert.throws(()=>validateAdminProfileChanges({...values,[k]:'x'},p));assert.throws(()=>validateAdminProfileChanges({...values,username:'admin'},p));assert.throws(()=>validateAdminProfileChanges({...values,first_name:'line\nbreak'},p));assert.throws(()=>validateAdminProfileChanges({...values,username:'a-b'},p));
 const calls=[],client={rpc:async(name,args)=>{calls.push({name,args});return{data:p};},auth:new Proxy({},{get(){throw Error('Auth APIs excluded');}})};
 await saveAdminProfile(client,p,values);assert.equal(calls.length,1);assert.equal(calls[0].name,'admin_save_profile');assert.equal(calls[0].args.p_target,p.user_id);assert.equal(calls[0].args.p_expected,p.snapshot);assert.deepEqual(Object.keys(calls[0].args.p_changes).sort(),['first_name','last_name','username']);
 await assert.rejects(saveAdminProfile(client,p,values,null,()=>false),/ACCOUNT_CHANGED/);assert.equal(calls.length,1);await assert.rejects(saveAdminProfile(client,p,values,{type:'text/html',size:10}),/PNG/);assert.equal(calls.length,1);await assert.rejects(saveAdminProfile(client,{...p,user_id:'wrong'},values),/дахин/);
});
