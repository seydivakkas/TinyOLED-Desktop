import { BrowserApp } from '../browser_app.js';

export class CryptoTickerApp extends BrowserApp {
  static NAME='crypto'; static LABEL='Kripto'; static ICON='crypto';
  constructor(onExit){super(onExit,{title:'Kripto',mode:'NET'});this.coins=[];this.refreshed=0;this.refresh();}
  async refresh(){
    await this.task(async()=>{
      const url='https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true';
      const r=await fetch(url,{headers:{accept:'application/json'}}); if(!r.ok) throw new Error(`CoinGecko ${r.status}`);
      const d=await r.json();
      this.coins=[
        ['BTC',`$${Number(d.bitcoin.usd).toLocaleString()}`],
        ['ETH',`$${Number(d.ethereum.usd).toLocaleString()}`],
        ['SOL',`$${Number(d.solana.usd).toLocaleString()}`],
        ['24h BTC',`${Number(d.bitcoin.usd_24h_change).toFixed(1)}%`]
      ]; this.refreshed=Date.now(); this.status='canli';
    },'cekiliyor');
  }
  onSel(){this.refresh();}
  draw(fb){this.drawHeader(fb,'NET');this.drawRows(fb,this.coins.length?this.coins:[['Durum','bekle'],['Kaynak','CoinGecko']]);this.footer(fb,'SEL yenile');}
}
