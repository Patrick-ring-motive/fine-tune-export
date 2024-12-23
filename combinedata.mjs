import { writeFile,readFile } from 'node:fs/promises';
import { Buffer } from 'node:buffer';



async function fetchText(){return await(await fetch(...arguments)).text();}
async function zfetchText(){try{return fetchText(...arguments)}catch(e){return e.message;}}
const zreadFile=async function(){try{return await readFile(...arguments);}catch(e){if(arguments[1]?.encoding||typeof arguments[1]=='string'){return e.message;}return Buffer.from(e.message);}}
const zwriteFile=async function(){try{return await writeFile(...arguments);}catch(e){console.log(e);}};

let dataset=JSON.parse(await zreadFile('./dataset/dataset.json','utf-8'));
let pdataset=JSON.parse(await zreadFile('./pdataset2/pdataset2.json','utf-8'));
let cdataset=[...dataset,...pdataset];
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
zwriteFile('./cdataset2/cdataset2.json',JSON.stringify(cdataset));
