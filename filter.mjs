import { writeFile,readFile } from 'node:fs/promises';
import { Buffer } from 'node:buffer';
import { jsonrepair } from 'jsonrepair';


async function fetchText(){return await(await fetch(...arguments)).text();}
async function zfetchText(){try{return fetchText(...arguments)}catch(e){return e.message;}}
const zreadFile=async function(){try{return await readFile(...arguments);}catch(e){if(arguments[1]?.encoding||typeof arguments[1]=='string'){return e.message;}return Buffer.from(e.message);}}
const zwriteFile=async function(){try{return await writeFile(...arguments);}catch(e){console.log(e);}};
JSON.zparse = function zparse(){
    try{
        return JSON.parse(...arguments);
    }catch(e){
        try{
            return JSON.parse(jsonrepair(...arguments));
        }catch{
            return e;
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

const file = await zreadFile('rawdata/rawdata.json','utf-8');
let list = Object.entries(JSON.zparse(file));

list = list.map(x =>[x[0],x[1].split('\n')
                                                  .filter(x => ~x.search(/s>|INST\]/)||!~x.search(/\{|\}|jQuery|;$/))
                                                  .join('\n')]);
let rawdata2 = Object.fromEntries(list);
                     console.log(rawdata2);
zwriteFile('rawdata2/rawdata2.json',JSON.stringify(rawdata2));