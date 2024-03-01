function spellDeck(selected_class, spellListName, listDesc) {

    const currentLoadout = [];

    this.createCards = (spells) => {
        for (let i = 0; i < spells.length; i++){
            const spellRow = $(` 
                <tr>
                    <td>
                        <p class = "card-text">${spells[i][0]}</p>
                    </td>
                    <td>
                        <p class = "card-text">${spells[i][1]}</p>
                    </td>
                    <td>
                        <p class = "card-text">${spells[i][2]}</p>
                    </td>
                    <td>
                        <p class = "card-text">${spells[i][3]}</p>
                    </td>
                    <td>
                        <p class = "card-text">${spells[i][4]}</p>
                    </td>
                    <td>
                        <a class = "spell-adder" href = "#" data-index = "${i}">Add/Remove</a>
                    </td>
                </tr>
            `);
            $('#spell-container tbody').append(spellRow);

        }

        //add spell to active loadout
        $('.spell-adder').on('click',function() {
            //can access index because of the buttons data-index attribute
            var index = $(this).data('index');
            var spellName = spells[index][0];
            var spellIndex = currentLoadout.indexOf(spellName); //is spellname in loadout already
            //returns -1 if not in list
            if (spellIndex === -1) {
                currentLoadout.push(spellName);
            } else {
                currentLoadout.splice(spellIndex, 1);
            }
            console.log(currentLoadout);

            //adding spells actively in loadout to top of screen
            $("#chosen-spells tbody").empty()
            for (let i =0; i < currentLoadout.length; i++) {
         
                const chosenSpell = $(`<tr><td>${currentLoadout[i]}</td></tr>`);
                $("#chosen-spells tbody").append(chosenSpell)
            }
        }); 
        

    }

    //submit the loadout to backend
    $("#post-loadout").on('click', _ => {
        console.log(currentLoadout)
        $.post('/api/post_loadout', {
            loadout:currentLoadout,
            spell_list_name:spellListName,
            list_desc:listDesc
        })
    })

    this.fetchSpells = () => {
        if (selected_class == 'fighter' || selected_class == 'rogue') {
            selected_class = 'Wizard'
        }
        $.get('/api/class_spells', {
            selected_class : selected_class,
        }, (data) => {
            this.createCards(data);
        })
    }

} 