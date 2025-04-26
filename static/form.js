//model表示
import * as Live2DCubismFramework from './live2dcubismframework.js';

async function loadModel() {
    const model = await Live2DCubismFramework.Live2DModelWebGL.loadModel("/static/model/gpt.model3.json");
    // モデルをステージに追加するコードもここでやる
}
loadModel();

// 入力エリアの高さを自動で広げる
document.addEventListener("DOMContentLoaded", function () {
    const textarea = document.getElementById("content");

    textarea.addEventListener("input", function () {
        this.style.height = "auto";
        this.style.height = this.scrollHeight + "px";
    });
});

//投稿送信
document.getElementById("diary-form").addEventListener("submit", async function (e) {
    e.preventDefault(); //ページリロードをstop

    //titleと本文を取り出す
    const title = document.getElementById("title").value;
    const content = document.getElementById("content").value;
    ///itemsにデータをjsonにして送る
    const response = await fetch("/items", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ title, content })
    });

    //投稿失敗時
    if (!response.ok) {
        alert("Upload failed(._.)");
        return;
      }
  
    const result = await response.json();
    alert("post diary");
    ///listに自動で移動
    window.location.href = "/list";
  });


  