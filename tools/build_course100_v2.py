"""Build reviewed native course documents from the new day map, not the old ordering."""
import json,pathlib,copy,hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
old=json.loads((ROOT/'study-plan.json').read_text())
if old['version']!=1:old=json.loads((ROOT/'audit/course100-v2/legacy-plan.json').read_text())
else:(ROOT/'audit/course100-v2/legacy-plan.json').write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n')
problems=json.loads((ROOT/'audit/course100-v2/reference-inventory.json').read_text())
lessons=json.loads((ROOT/'audit/course100-v2/tutorial-sections.json').read_text())
by={(p['source'].lower(),p['ref'].lower()):p for p in problems}
by.update({('cses',p['ref']):p for p in problems if p['source']=='CSES'})
topics={t['id']:t for t in lessons}
for t in json.loads((ROOT/'audit/course100-v2/setup-tutorials.json').read_text()):topics[t['id']]=t
primers=json.loads((ROOT/'audit/course100-v2/beginner-primers.json').read_text())
bank={}
for line in (ROOT/'audit/course100-v2/quiz-bank.tsv').read_text().splitlines():
 key,qmn,qen,omn,oen,ans,emn,een=line.split('|');bank[key]=(qmn,qen,omn.split('~'),oen.split('~'),int(ans),emn,een)
phases=[('Орчин ба программын суурь','Environment and programming foundations'),('Эрэмбэ, хайлт, сонголт','Order, search and selection'),('Муж ба өгөгдлийн бүтэц','Ranges and containers'),('Бүрэн хайлт ба тооцоолол','Complete search and arithmetic'),('Dynamic Programming','Dynamic Programming'),('Графын загвар ба traversal','Graph models and traversal'),('Зам, component, мод','Paths, components and trees'),('Tree query ба range query','Tree and range queries'),('Бүтэц сонгох ба батлах','Choosing structures and proving choices'),('String ба бие даасан дадлага','Strings and independent practice')]
review={7,10,19,20,30,39,40,49,50,59,60,65,70,79,80,88,90,95,97,98,99,100}
rows=[];manifest=[]
def quiz(topic,day,lang,suffix='core',reference_day=None):
 key={47:'reconstruction',62:'stale-heap',74:'lca-jump',75:'lca-path',92:'z-function'}.get(reference_day or day,'setup'if topic.startswith('cpp-')else topic)
 qmn,qen,omn,oen,ans,emn,een=bank[key];texts=oen if lang=='en'else omn
 option_ids=['o-'+hashlib.sha256((key+'|'+t).encode()).hexdigest()[:16]for t in oen]
 options=[{'id':option_ids[i],'text':t}for i,t in enumerate(texts)]
 shift=day%len(options);options=options[shift:]+options[:shift]
 return {'type':'quiz','quizId':f'day-{day:03d}-{suffix}','question':qen if lang=='en'else qmn,'options':options,'answerId':option_ids[ans],'explanation':een if lang=='en'else emn}
for d,line in enumerate((ROOT/'audit/course100-v2/day-map.tsv').read_text().splitlines(),1):
 topic,mn,en,source,ref=line.split('|');phase=(d-1)//10;local=source=='local';p=None if local else by.get((source,ref.lower()))
 if not local and not p:raise ValueError((d,source,ref))
 required=[]if local else [str(p['number'])]
 secondary={10:'1069',20:'1640',40:'1623',50:'1638',60:'1668',80:'1648',90:'1675',97:'1753'}.get(d)
 extra=by.get(('cses',secondary))if secondary else None
 if extra:required.append(str(extra['number']))
 kind='review'if d in review else'study'
 if d in [10,20,40,50,60,80,90,97]:kind='assessment'
 review_days=[x for x in ([d-7,d-21]if d%7==0 and d>21 else[d-3,d-7])if x>0][:2]
 key='setup'if topic.startswith('cpp-')else topic
 qmn,qen,*_=bank[key]
 focusmn=f'{mn}. Өдрийн төгсгөлд «{qmn}» гэсэн асуултыг код харалгүй тайлбарлаж чаддаг болно.'
 focusen=f'{en}. By the end, explain without reference code: {qen}'
 day={'day':d,'phase':phase+1,'phaseName':phases[phase][0],'phaseNameEn':phases[phase][1],'tutorials':[topic],'title':mn,'titleEn':en,'goal':focusmn,'goalEn':focusen,'observations':[],'required':required,'priority':required[:],'challenge':[],'minutes':45 if d<6 or kind=='review'else 90 if kind=='assessment'else 75,'kind':kind,'reviewDays':review_days,'checklist':['Өдрийн гол асуултыг өөрийн үгээр тайлбарласан.','Үндсэн дасгалын шийдлийг жишээ болон захын тохиолдлоор шалгасан.','Тестийн тайлбарыг уншаад алдаатай ойлголтоо зассан.'],'checklistEn':['Explain the focus question in my own words.','Check the main exercise with samples and boundary cases.','Read quiz feedback and correct my misconception.']}
 if local:day['localExercise']=ref
 versions={}
 explicit={1:[0,1,2,3],2:[1,2],3:[0,3],4:[0],5:[0],6:[0,1,2],7:[1,2],8:[0,1],9:[0],11:[1],12:[0,1,2,3],17:[0],20:[1],29:[0,1],31:[0,1,2,3],32:[0],33:[1],34:[2,3],37:[1,2],38:[0,1],40:[2,3],41:[0],42:[0],44:[1,2,3],45:[0,1,2],47:[0],48:[0,1,2,3],52:[1],59:[1,2],61:[1],65:[1],67:[0,1,2],68:[0],69:[1],71:[0,1,2,3],72:[4,5,6],73:[0],74:[1],75:[2,4],78:[2],79:[2],81:[2],82:[0,1],83:[1],85:[0],87:[0,1,2],91:[1,5],92:[4],94:[4,5],95:[0,1],96:[0,1,2,3,4]}
 selected=explicit.get(d,[i for i,sec in enumerate(topics[topic]['sections'])if not any(w in sec['title'].lower()for w in ['дасгал','бие даа'])])
 day['completionMode']='daily-practice';day['tutorialSections']={topic:selected}
 for lang in ['mn','en']:
  english=lang=='en';title=en if english else mn;goal=focusen if english else focusmn
  blocks=[{'type':'p','text':goal}]
  source=topics[topic].get('translations',{}).get('en',topics[topic])if english else topics[topic]
  for section_index in selected:
   blocks.append({'type':'rich','content':[{'text':source['sections'][section_index]['title'],'href':'#tutorial/'+topic+'/part/'+str(section_index),'marks':[]}]})
  blocks.append({'type':'p','text':'Read the assigned sections, not necessarily the whole chapter today. Use the tutorial’s section-by-section mode and Mark section read. Daily completion requires this reading record, core practice and your daily checks; it does not declare whole-topic mastery.'if english else'Өнөөдөр зөвхөн заасан хэсгүүдэд төвлөр; бүх бүлгийг нэг өдөр дуусгах албагүй. Хичээлийн «Хэсэг хэсгээр» горимын «Энэ хэсгийг уншсан» товчоор тэмдэглэ. Өдрийн completion нь энэ тэмдэглэл, үндсэн дасгал, өөрийн checklist-ээс бүрдэнэ; сэдвийг бүхэлд нь эзэмшсэн гэж зарлахгүй.'})
  if review_days:
   blocks.append({'type':'p','text':'Before reopening notes, recall one decision, invariant or counterexample from the linked earlier day. A forgotten step is a review target, not failure.'if english else'Өмнөх өдрийн тэмдэглэлээ нээхээс өмнө нэг сонголт, invariant эсвэл эсрэг жишээг сэргээн тайлбарла. Мартсан хэсгээ дахин үзэх зорилго болго.'})
   blocks.append({'type':'rich','content':[{'text':('Review day 'if english else'Давтах өдөр ')+str(x),'href':'#plan/'+str(x),'marks':[]}for x in review_days]})
  practice=[{'type':'p','text':'Try a small case by hand, then write a simple correct solution before optimizing. If stuck without a new idea, inspect one hint, close it and implement independently. Revisit a previously solved task using today’s method instead of merely ticking its old solved badge.'if english else'Эхлээд жижиг жишээг гараар бодож, энгийн зөв шийдлээ байгуул. Шинэ санаа гарахгүй гацвал нэг hint үзээд хааж, өөрөө хэрэгжүүл. Өмнө бодсон бодлого таарвал хуучин solved тэмдэгт найдалгүй өнөөдрийн аргаар дахин тайлбарлаж шалга.'}]
  if p:
   for problem_key in required:practice.append({'type':'problem','problemKey':problem_key})
  else:
   practice.append({'type':'p','text':('Compile and run the language-mode probe in the setup tutorial, then change one output line and rebuild. Record which compiler and shell you used.'if d==1 else'Read two integers and print their sum. For input2 3, print5 and a newline. Check0 0 and a negative value too.')if english else('Орчны зааврын language-mode шалгах программыг compile/run хийгээд нэг гаралтын мөрийг өөрчилж дахин build хий. Ашигласан compiler, shell-ээ тэмдэглэ.'if d==1 else'Хоёр бүхэл тоо уншиж нийлбэрийг нь хэвлэ. 2 3 оролтод 5 болон шинэ мөр гаргана. 0 0 болон сөрөг утгаар мөн шалга.')})
  if d==2:
   practice.extend([{'type':'p','text':'int a,b нь хоёр бүхэл тооны хувьсагч. cin >> a >> b оролтоос уншина; cout нийлбэр ба шинэ мөр хэвлэнэ. Энэ дасгалын a,b нь -1000-аас1000 тул int хангалттай. Эхлээд энэ хэсгийг ойлгоод бүтэн main дотор байрлуул.'if not english else'int a,b declares two integers. cin >> a >> b reads them; cout prints their sum and a newline. Inputs are between -1000 and1000, so int fits. Understand these operations before placing them in main.'},
    {'type':'code','language':'C++17','text':"#include <iostream>\n\nusing namespace std;\n\nint main() {\n    int a, b;\n    cin >> a >> b;\n    cout << a + b << '\\n';\n}\n"},
    {'type':'code','language':'Input','text':'2 3\n'},{'type':'code','language':'Output','text':'5\n'}])
  if str(d)in primers:
   primer=primers[str(d)];practice.extend([{'type':'p','text':primer['en'if english else'mn']},{'type':'code','language':'C++17','text':primer['fragment']},{'type':'p','text':'Place the fragment in this complete program, then test the example and one boundary case.'if english else'Энэ хэсгийг дараах бүтэн программ дотор байрлуулж, жишээ болон нэг захын тохиолдлоор шалга.'},{'type':'code','language':'C++17','text':primer['code']},{'type':'code','language':'Input','text':primer['input']},{'type':'code','language':'Output','text':primer['output']}])
  if d==47:practice.insert(0,{'type':'note','text':'Frog2 requires only the minimum cost in judge output. Reconstruct a path for local verification, but do not print extra path text to stdout when submitting.'if english else'Frog2-ийн judge гаралт нь зөвхөн хамгийн бага зардал. Зам сэргээхийг локал шалгалтад хий; submit хийх stdout-д нэмэлт зам хэвлэж болохгүй.'})
  if d==63:practice.insert(0,{'type':'note','text':'Cycle Finding asks for any negative cycle, not only one reachable from a specified source. An all-zero distance initialization models a super-source to every vertex.'if english else'Cycle Finding нь өгсөн эхлэх оройгоос хүрэхийг биш, графын аль ч negative cycle-ийг асууна. Бүх distance-ийг 0-оор эхлүүлэх нь бүх оройтой холбосон super-source-той адил.'})
  if d==87:practice.insert(0,{'type':'note','text':'Two Sets II has n up to500: a 2^n mask table is infeasible. Use this as a deliberate method-selection exercise and return to Knapsack, rather than forcing Bitmask DP.'if english else'Two Sets II-д n нь500 хүрнэ: 2^n mask массив боломжгүй. Bitmask DP-г хүчээр хэрэглэхийн оронд арга сонгох дасгал болгож Knapsack-аа сэргээн үз.'})
  if d==96:practice.insert(0,{'type':'note','text':'Cluedo is a grader-function task. Follow its library interface; this is not a plain stdin/stdout executable. Use the provided local grader instead of inventing a main protocol.'if english else'Cluedo нь grader-ийн функцтэй бодлого. Өгсөн library interface-ийг дагана; жирийн stdin/stdout executable биш. Өөрөө main protocol зохиохын оронд өгсөн local grader-ийг ашигла.'})
  check=[quiz(topic,d,lang)]
  if kind in ['review','assessment']and d>3:
   previous=next((rows[x-1]for x in review_days if rows[x-1]['tutorials'][0]!=topic),next((x for x in reversed(rows)if x['tutorials'][0]!=topic),rows[0]))
   check.append(quiz(previous['tutorials'][0],d,lang,'retrieval',previous['day']))
  check.append({'type':'p','text':'This is retrieval practice, not a secure exam or automatic proof of mastery. Retry after understanding the feedback. The daily checklist records your own review.'if english else'Энэ тест нь ойлголтоо сэргээх дадлага; хамгаалалттай шалгалт эсвэл эзэмшсэний автомат баталгаа биш. Тайлбарыг ойлгосныхоо дараа дахин оролдоорой. Өдрийн checklist нь өөрийн хяналтын тэмдэглэл.'})
  versions[lang]={'title':title,'summary':goal,'sections':[{'title':'1. Focus and retrieval'if english else'1. Зорилго ба сэргээн санах','blocks':blocks},{'title':'2. Deliberate practice'if english else'2. Бодож хэрэгжүүлэх','blocks':practice},{'title':'3. Check understanding'if english else'3. Ойлголтоо шалгах','blocks':check}]}
 day['document']={'id':f'course-day-{d:03d}','order':d,'category':'100 days','levelKey':'beginner'if d<=40 else'intermediate','priorityLevel':'medium','automaticDemo':False,**versions['mn'],'translations':{'en':versions['en']}}
 rows.append(day)
 manifest.append({'day':d,'tutorial':topic,'problem':None if not p else{'id':p['id'],'number':p['number'],'title':p['title'],'url':p['url'],'rating':p.get('rating')},'kind':kind,'reviewDays':review_days,'selectionRationale':f'New sequence focus: {en}. One core task avoids the former uniform3-task load; review repeats demand a new explanation/test, not a new solved date.','secondaryProblems':[]if not extra else[{'id':extra['id'],'number':extra['number'],'title':extra['title'],'url':extra['url'],'rating':extra.get('rating')}],'selectionStatus':'contextually reviewed against task identity, prerequisites and task-specific method caveats'})
plan={'id':old['id'],'version':2,'title':'100 өдрийн шаталсан дадлага','titleEn':'100 days of purposeful practice','timezone':old['timezone'],'days':rows}
(ROOT/'study-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
(ROOT/'audit/course100-v2/selection-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print({'days':len(rows),'native_quizzes':sum(sum(b['type']=='quiz'for b in s['blocks'])for d in rows for s in d['document']['sections']),'unique_core_tasks':len(set(k for d in rows for k in d['required']))})
