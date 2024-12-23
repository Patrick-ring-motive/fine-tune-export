import { writeFile,readFile } from 'node:fs/promises';
import { Buffer } from 'node:buffer';
import { jsonrepair } from 'jsonrepair';
import { parse } from 'dirty-json';

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

JSON.zstringify = function zparse(){
    try{
        return JSON.stringify(...arguments);
    }catch(e){
        const a = Object.getOwnPropertyNames(e);
        const obj = {};
        for(const x of a){
            obj[x] = e[x];
        }
        return JSON.stringify(obj);
    }
}

const canparse = function(json){
    try{
        JSON.parse(jsonrepair(json));
        return true;
    }catch{
         try{
                dJSON.parse(json);
                return true;
            }catch{
                try{
                    parse(json);
                    return true;
                }catch{
                    return false;
                }
            }
    }
}

const caneval = function(json){
    try{
        eval(json);
        return true;
    }catch{
        return false;
    }
}

const file = await zreadFile('fromatted.json','utf-8');
let list = file.split('```').filter(x=>x.startsWith('json')).map(x=>x.slice(4));
let parseable = list.filter(x=>canparse(x));
let unparsed = list.filter(x=>!canparse(x));
console.log(parseable.length);
console.log(unparsed.map(x=>JSON.zparse(x)));
await zwriteFile('dataset2/parseable.json',JSON.stringify(parseable));
await zwriteFile('dataset2/unparsed.json',JSON.stringify(unparsed));