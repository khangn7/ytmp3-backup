const span_search_count = document.getElementById("span-search-count");

const input_search_bar = document.getElementById("input-search-bar");
const button_search = document.getElementById("button-search");

const div_search_results = document.getElementById("div-search-results");


button_search.addEventListener("click", () => {
  if (input_search_bar.value != "")
  {
    displaySearchResults(input_search_bar.value);
  }
});

const server_url = "https://ytmp3.khangn7.repl.co/";

async function postToServer(endpoint, payload)
{
  let response = await fetch(server_url + endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      "payload": payload
    })
  });

  let data = await response.json(); 
  console.log(data);
  
  return data["payload"];
}

async function getSearchResults(search_str)
{
  return await postToServer("getSearchResults", search_str);
}

async function displaySearchResults(search_str)
{
  let results = await getSearchResults(search_str);
  for (let i = 0; i < results.length; i++)
  {
    let div_video = document.createElement("div");
    div_video.className = "div-video";
    
    div_video.innerHTML =  `<p>title: ${results[i]["videoTitle"]}</p><p>channel: ${results[i]["channelTitle"]}</p><img src="${results[i]["thumbnail"]}" width="70%"><button id="${"button-" + results[i]["videoId"]}">download</button>`; 
    
    div_search_results.appendChild(div_video);

    document.getElementById("button-" + results[i]["videoId"]).addEventListener("click", getDownloadLink);
  }

  span_search_count.innerHTML = Number(span_search_count.innerHTML) + 1;
}

async function getDownloadLink(e)
{
  let targetId = e.target.id,
      videoId = targetId.slice(targetId.indexOf("-") + 1);
  // url is url to resource on server
  let url = await postToServer("download", videoId);
  // clear videos and create link
  div_search_results.innerHTML = `<br><br><a id="download-link" href="download/${url}" download>click to download mp3 file</a>*can only press once`;
  
  div_search_results.innerHTML += "<br><button id='button-back'>go back</button>";
  document.getElementById("button-back").addEventListener("click", async () => {
    await postToServer("delete", 0);
    window.location = server_url;
  });
  
  console.log(div_search_results.innerHTML);
}
