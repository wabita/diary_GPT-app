//過去の日記表示
window.addEventListener("load", function() {
    const diaryEntries = JSON.parse(localStorage.getItem("diaryEntries")) || [];

    const diaryList = document.getElementById("diary-list");
    
    if (diaryEntries.length === 0) {
        const noEntries = document.createElement("p");
        noEntries.textContent = "まだ日記はありません。";
        diaryList.appendChild(noEntries);
    } else {
        diaryEntries.forEach(entry => {
            const entryDiv = document.createElement("div");
            entryDiv.classList.add("diary-entry");
            const formattedContent = entry.content.replace(/\n/g, "<br>");

            // 日付にフォントクラスを追加
            const entryDate = document.createElement("h2");
            entryDate.classList.add("dotgothic16-regular");  // フォントクラス追加
            entryDate.textContent = entry.date;

            // 日記内容にフォントクラスを追加
            const entryContent = document.createElement("p");
            entryContent.classList.add("dotgothic16-regular");  // フォントクラス追加
            entryContent.innerHTML = formattedContent;
            
            entryDiv.appendChild(entryDate);  // 日付を追加
            entryDiv.appendChild(entryContent);  // 日記内容を追加
            entryDiv.innerHTML += `<hr>`;
            diaryList.appendChild(entryDiv);
        });
    }
});