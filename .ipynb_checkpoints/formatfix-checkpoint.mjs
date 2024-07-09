import { writeFile,readFile } from 'node:fs/promises';
import { Buffer } from 'node:buffer';



async function fetchText(){return await(await fetch(...arguments)).text();}
async function zfetchText(){try{return fetchText(...arguments)}catch(e){return e.message;}}
const zreadFile=async function(){try{return await readFile(...arguments);}catch(e){if(arguments[1]?.encoding||typeof arguments[1]=='string'){return e.message;}return Buffer.from(e.message);}}
const zwriteFile=async function(){try{return await writeFile(...arguments);}catch(e){console.log(e);}};

let f=await zreadFile('fromatted.json','utf-8');
let cleaned = f.split('```json').map(x=>x.split('```')[0]).slice(1);
let objs=[];
for(let i=0;i<cleaned.length;i++){
try{
    objs.push(JSON.parse(cleaned[i]));
}catch(e){
    try{
        objs.push(eval(cleaned[i]));
    }catch(e){
            try{
               let pairs=(eval(extractPairs(cleaned[i])));
                for(let o=1;o<pairs.length;o++){
                    (pairs[o]??{}).request??=pairs[o-1]?.request;
                    (pairs[o]??{}).response??=pairs[o-1]?.response;
                }
                objs.push([...new Set(pairs)]);
            }catch(e){
                console.log(e);
            }
    }
    
}
}

objs=objs.map(x=>x.data?x.data:x).flat();
objs.forEach(x=>{
    x.response=x.response?.of?x.response.join('↵'):`${x.response}`.replaceAll('\n','↵');
    x.request=`${x.request}`.replaceAll('\n','↵');
});
let pdataset=[];
objs.forEach(x=>{
    pdataset.push(datumf(x.request,x.response));
});
console.log(pdataset);
zwriteFile('./pdataset/pdataset.json',JSON.stringify(pdataset));

function extractPairs(s){
   let r=`[${s.split('\n').filter(x=>x.match(/request|response/)).map(x=>`{${x.replace(/[\[\]\{\}\n]/g,'').trim().replace(/[,]$/g,'').replace(/\\["]$/g,'"').replace(/([^,"])$/g,'$1"').replace(/(:["])$/g,':""')}}`).join(',\n')}]`;
   // console.log(r);
    return r
}

function datumf(req,res){
    return `<s>[INST] ${req} [/INST] ${res} </s>`;
}