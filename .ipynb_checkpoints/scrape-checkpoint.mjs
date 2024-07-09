import { writeFile,readFile } from 'node:fs/promises';
import { Buffer } from 'node:buffer';

console.log(process.version);

async function fetchText(){return await(await fetch(...arguments)).text();}
async function zfetchText(){try{return fetchText(...arguments)}catch(e){return e.message;}}
const zreadFile=async function(){try{return await readFile(...arguments);}catch(e){if(arguments[1]?.encoding||typeof arguments[1]=='string'){return e.message;}return Buffer.from(e.message);}}
const zwriteFile=async function(){try{return await writeFile(...arguments);}catch(e){console.log(e);}};
globalThis.RegExp.prototype.ztest=function(s){try{return this.test(String(s));}catch(e){return false;}};

let systemStorage={};

try{
   systemStorage = JSON.parse(await zreadFile('systemStorage.json','utf-8'));
}catch(e){
   zwriteFile('systemStorage.json',JSON.stringify(systemStorage));
   console.log(e);
}

systemStorage.getItem=function(key){
    return decodeURIComponent(systemStorage[key]);
}

systemStorage.setItem=function(key,val){
    systemStorage[key]=encodeURIComponent(val);
    zwriteFile('systemStorage.json',JSON.stringify(systemStorage));
}

let dataset=[];
let rawdata={};

const list = JSON.parse(systemStorage.getItem('usaaef'));
  let retry=true;
  while(retry){
      let errs=0;
      const gatherFiles=[]; 
      for(let i=0;i<list.length;i++){
                if(list[i].endsWith('.pdf')){continue;}
                const title=list[i].replace(/[^a-zA-Z0-9\.]+/g,'-');
                let content=await zreadFile(title,'utf-8');
                if(/^(ENOENT|429|System Error)/.ztest(content)){
                    (async ()=>console.log(list[i]))();
                    gatherFiles.push((async ()=>{
                        let txt = await zfetchText(list[i]);
                        txt = stripDOM(txt);
                        if(/^(ENOENT|429|System Error)/.ztest(txt)){
                            errs++;
                            console.warn(`error on ${title}`);
                            return;
                        }
                        await zwriteFile(title,txt);
                    })());
                }else{
                    try{btoa(content)}catch(e){continue;}
                    rawdata[list[i]]=content;
                    dataset.push(datumFormat(list[i],content));
                }
      }
     await Promise.all(gatherFiles);
     console.log('done');
    retry=errs;
  }
console.log(dataset.length);
zwriteFile('./dataset/dataset.json',JSON.stringify(dataset));
zwriteFile('./rawdata/rawdata.json',JSON.stringify(rawdata));
console.log('written?');
function stripDOM(text){
  text=`${text}`;
  if(text.includes('<article')){
    text = '<article'+text.split('<article')[1];
  }
  if(text.includes('<main')){
    text = '<main'+text.split('<main')[1].split('</main>')[0];
  }
    if(text.includes('<body')){
    text = '<body'+text.split('<body')[1].split('</body>')[0];
  }
  text = text.replace(/<style.*\/style>/g,'')
    .replace(/<script.*\/script>/g,'')
                .replace(/<header.*\/header>/g,'')
    .replace(/<footer.*\/footer>/g,'')
                .replace(/<ul.*\/ul>/g,'')
    .replace(/<ol.*\/ol>/g,'')
                .replace(/<nav.*\/nav>/g,'')
    .replace(/<[^>]*>/g,'');
 
  text = text.replaceAll('\t',' ');
  text=text.replaceAll('\n ','\n');
 
  let count = 0;
  let text2=text.replace(/ +/g,' ');
  while((text2!=text)&&(count<100)){
  text=text2;
   text2 = text.replaceAll('  ',' ');
    count++;
  }
  text=text2.replaceAll('\n ','\n');
 
  count = 0;
  text2=text.replaceAll('\n\n','\n');
  while((text2!=text)&&(count<100)){
    text=text2;
   text2 = text.replaceAll('\n\n','\n');
    count++;
  }
  text=text2;
  text=text.replace(new RegExp('(\r*\n)+', 'mg'),'\n');
  text.includes('Print Page')&&(text=text.split('Print Page')[1]);
text=text.replace(`Get to Know Us
Meet the Team
Meet the Board
`,'').replace('About Us','').replace('Meet the Team','');
  text=text.split('Contact Us')[0];
 return text.trim();
}
 
function datumFormat(url,str){
    return `<s>[INST] What is the raw information found at "${url}", a web page from tge USAA Educational Foundation?  [/INST] ${str} </s>`;
}