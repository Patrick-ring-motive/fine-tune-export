import { writeFile,readFile } from 'node:fs/promises';
import { Buffer } from 'node:buffer';



async function fetchText(){return await(await fetch(...arguments)).text();}
async function zfetchText(){try{return fetchText(...arguments)}catch(e){return e.message;}}
const zreadFile=async function(){try{return await readFile(...arguments);}catch(e){if(arguments[1]?.encoding||typeof arguments[1]=='string'){return e.message;}return Buffer.from(e.message);}}
const zwriteFile=async function(){try{return await writeFile(...arguments);}catch(e){console.log(e);}};

let cdataset=JSON.parse(await zreadFile('./cdataset/cdataset.json','utf-8'));

cdataset.forEach((item,i)=>{
    if(item.includes('JavaScript')){
       cdataset.splice(i,1);
    }
});


cdataset.forEach((item,i)=>{
    if(item.includes('if (document.readyState')){
       cdataset[i]=`${cdataset[i].split('if (document.readyState')[0]} </s>`;
    }
});
zwriteFile('./cdataset/cdataset.json',JSON.stringify(cdataset));
