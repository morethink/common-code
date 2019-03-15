const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({
        headless: false
    });
    const page = await browser.newPage();
    await page.goto('https://www.cnblogs.com/morethink/p/6525216.html');
    await page.setViewport({
        width: 1200,
        height: 800
    });
    //获取页面Dom对象
    let body = await page.$('#cnblogs_post_body');
    //调用页面内Dom对象的 screenshot 方法进行截图
    await body.screenshot({
        path: '2.png'
    });
    await browser.close();
})();