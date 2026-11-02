import fs from'node:fs';import{joiFixture}from'./joi-url-fixture.mjs';
export async function joiStatementFixture(rows=JSON.parse(fs.readFileSync('audit/joi-statements/before-targets.json'))){
 const db=await joiFixture(rows),snapshot=JSON.parse(fs.readFileSync('audit/joi-statements/validation-functions.json'));
 for(const name of['normalize_problem_source','valid_task_url','validate_priority_metadata','validate_native_problem_statement','validate_native_problem_editorial','validate_learning_problem','admin_save_problem','get_catalog','get_admin_catalog'])await db.exec(snapshot.functions.find(f=>f.name===name).definition);
 return db;
}
