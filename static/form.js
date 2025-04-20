// 入力エリアの高さを自動で広げる
document.addEventListener("DOMContentLoaded", function () {
    const textarea = document.getElementById("content");

    textarea.addEventListener("input", function () {
        this.style.height = "auto";
        this.style.height = this.scrollHeight + "px";
    });
});