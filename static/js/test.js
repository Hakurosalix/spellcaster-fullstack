function spellDeck(selected_class, spellListName, listDesc) {

    const currentLoadout = [];

    this.createCards = (spells) => {
        for (let i = 0; i < spells.length; i++){
                const spellCard = $(`
                <div class = "card">
                    <div class = "card-body">
                        <div class = "row">
                            <div class = "col-md-2">
                                Spell
                            </div>
                            <div class = "col-md-2">
                                Spell Level
                            </div>
                            <div class = "col-md-2">
                                Concentration
                            </div>
                            <div class = "col-md-2">
                                Ritual
                            </div>
                            <div class = "col-md-2">
                                Range
                            </div>
                            <div class = "col-md-2">
                                
                            </div>
                            
                        </div>  
                        <div class = "row">
                            <div class = "col-md-2">
                                <p class = "card-text">${spells[i][0]}</p>
                            </div>
                            <div class = "col-md-2">
                                <p class = "card-text">${spells[i][1]}</p>
                            </div>
                            <div class = "col-md-2">
                                <p class = "card-text">${spells[i][2]}</p>
                            </div>
                            <div class = "col-md-2">
                                <p class = "card-text">${spells[i][3]}</p>
                            </div>
                            <div class = "col-md-2">
                                <p class = "card-text">${spells[i][4]}</p>
                            </div>
                            <div class = "col-md-2">
                                <a class = "spell-adder" href = "#" data-index = "${i}">Add/Remove</a>
                            </div>
                            
                        </div>
                    </div>
                </div>`);
                $('#spell-container').append(spellCard)

        }
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
            $("#chosen-spells").empty()
            for (let i =0; i < currentLoadout.length; i++) {
         
                const p = $(`<p>${currentLoadout[i]}</p>`);
                $("#chosen-spells").append(p)
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