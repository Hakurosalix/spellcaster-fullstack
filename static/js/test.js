$(document).ready(function () {
    for (let i = 0; i < spellName.length; i++) {
        const p = document.createElement("p");
        p.innerHTML = (spellName[i]);
        $('#spell-container').append(p);
    }
});