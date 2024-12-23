import { writeFile,readFile } from 'node:fs/promises';
import { Buffer } from 'node:buffer';
import { jsonrepair } from 'jsonrepair';
import { parse } from 'dirty-json';

const Q = fn=>{
    try{return fn();}catch{return undefined;}
};

async function fetchText(){return await(await fetch(...arguments)).text();}
async function zfetchText(){try{return fetchText(...arguments)}catch(e){return e.message;}}
const zreadFile=async function(){try{return await readFile(...arguments);}catch(e){if(arguments[1]?.encoding||typeof arguments[1]=='string'){return e.message;}return Buffer.from(e.message);}}
const zwriteFile=async function(){try{return await writeFile(...arguments);}catch(e){console.log(e);}};

JSON.zparse = function zparse(json){
    try{
        return JSON.parse(json);
    }catch(e){
        try{
            return JSON.parse(jsonrepair(json));
        }catch{
            try{
                return parse(json);
            }catch{
                return e;
            }
        }
    }
}


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
                try{
                    objs.push(JSON.parse(cleaned[i]));
                }catch{
                    console.log(e);
                }
            }
    }
    
}
}

objs=objs.map(x=>x.data?x.data:x).flat().filter(x=>Q(()=>x.request)).filter(x=>!~String(Q(()=>x.response)).trim().search(/null|undefined/));
objs.forEach(x=>{
    //console.log(x);
    x.response=x.response?.of?x.response.join('↵'):`${x.response}`.replaceAll('\n','↵');
    x.request=`${x.request}`.replaceAll('\n','↵');
});
let pdataset=[];
objs.forEach(x=>{
    pdataset.push(datumf(x.request,x.response));
});
console.log(pdataset.length);
zwriteFile('./pdataset2/pdataset2.json',JSON.stringify(pdataset));

function extractPairs(s){
   let r=`[${s.split('\n').filter(x=>x.match(/request|response/)).map(x=>`{${x.replace(/[\[\]\{\}\n]/g,'').trim().replace(/[,]$/g,'').replace(/\\["]$/g,'"').replace(/([^,"])$/g,'$1"').replace(/(:["])$/g,':""')}}`).join(',\n')}]`;
    return r
}

function datumf(req,res){
    return `<s>[INST] ${req} [/INST] ${res} </s>`;
}