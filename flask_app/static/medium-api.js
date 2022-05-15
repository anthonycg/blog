// const { parse } = require('rss-to-json');
// // async await
// (async () => {

//     var rss = await parse('https://api.rss2json.com/v1/api.json?rss_url=https://medium.com/feed/@anthonycg_');
    
//     console.log(JSON.stringify(rss, null, 3));

// })();

// // Promise

// parse('https://api.rss2json.com/v1/api.json?rss_url=https://medium.com/feed/@anthonycg_').then(rss => {
//     console.log(JSON.stringify(rss, null, 3));
    
// });

async function medium() {
    response = await fetch("https://api.rss2json.com/v1/api.json?rss_url=https%3A%2F%2Fmedium.com%2Ffeed%2F%40anthonycg_%2F");
    coderData = await response.json();
    var recentStories = document.getElementById("recent-stories")
    console.log(coderData.items)
    for (let i=0;i < coderData.items.length -5;i++) {
        let row = document.createElement("tr")
        let name = document.createElement("td")
        name.innerHTML = coderData.items[i].title
        let author = document.createElement("td")
        author.innerHTML = coderData.items[i].author
        let varLink = document.createElement("a")
        varLink.href = coderData.items[i].link
        varLink.innerHTML = "Read Article"
        row.appendChild(name)
        row.appendChild(author)
        console.log(varLink)
        row.appendChild(varLink)
        recentStories.appendChild(row)
    }
    console.log()
    return coderData; }
    
    medium();


    