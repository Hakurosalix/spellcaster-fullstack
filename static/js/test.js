function spellDeck(all_spells) {
    //console.log('Received data:', all_spells);
    var spells =  JSON.parse(all_spells);

    for (let i = 0; i < spells.length; i++){
        for (let j = 0; j < spells[i].length; i++) {
            console.log(spells[i][j])
            const p = $(`<p>${spells[i][j]}</p>`);
            $('#spell-container').append(p)
        }
    }

} 