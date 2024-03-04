function spellTable(selected_class, spellListName, listDesc) {

    const currentLoadout = [];
    
    this.createTable = (spells) => {
        var activeSpellLevel = spells[0][1];
        $('#spell-container tbody').append(`<tr><td class = "tref"><br><h3>Level ${activeSpellLevel}<\h3></td>
        <td class = "tref"></td>
        <td class = "tref"></td>
        <td class = "tref"></td>
        <td class = "tref"></td>
        <td class = "tref"></td></tr>`);
        for (let i = 0; i < spells.length; i++){
            const spellRow = $(` 
                <tr>
                    <td class = "tref">
                    <span class="expand-desc" data-index="${i}" style="cursor: pointer;">${spells[i][0]}</span>
                    </td>
                    <td class = "tref">
                        <p class = "tref">${spells[i][1]}</p>
                    </td>
                    <td class = "tref">
                        <p class = "tref">${spells[i][2] === 1 ? 'Yes' : 'No'}</p>
                    </td>
                    <td class = "tref">
                        <p class = "tref">${spells[i][3] === 1 ? 'Yes' : 'No'}</p>
                    </td>
                    <td class = "tref">
                        <p class = "tref">${spells[i][4]}</p>
                    </td>
                    <td class = "tref">
                        <a class = "spell-adder" href = "#" data-index = "${i}">Add</a>
                    </td>
                </tr>
            `);
            const hiddenDescription = $(`<tr class = "expanded-view" id = "expanded-view${i}" data-index = "${i}" style = "display: none;">
                    <td colspan="6" class = "tref">
                        <br>
                        <h3>${spells[i][0]}</h3>
                        <br>
                        Level: ${spells[i][1]}
                        <br><br>
                        Concentration: ${spells[i][2] === 1 ? 'Yes' : 'No'}
                        <br><br>
                        Ritual: ${spells[i][3] === 1 ? 'Yes' : 'No'}
                        <br><br>
                        Range: ${spells[i][4]}
                        <br><br>
                        Components: ${spells[i][5]}
                        <br><br>
                        Duration: ${spells[i][6]}
                        <br><br>
                        Casting Time: ${spells[i][7]}
                        <br><br>
                        Classes: ${spells[i][8]}
                        <br><br>
                        School: ${spells[i][9]}
                        <br>
                        ${spells[i][10]}
                        </td></tr>
            `)
            console.log(spells[i][10])
            if (spells[i][1] != activeSpellLevel) {
                activeSpellLevel = spells[i][1];
                $('#spell-container tbody').append(`<tr><td class = "tref"><br><h3>Level ${activeSpellLevel}<\h3></td>
                <td class = "tref"></td>
                <td class = "tref"></td>
                <td class = "tref"></td>
                <td class = "tref"></td>
                <td class = "tref"></td></tr>`);
            }
            $('#spell-container tbody').append(spellRow);
            $('#spell-container tbody').append(hiddenDescription);

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

            //adding spells actively into loadout display
            $("#chosen-spells tbody").empty()
            for (let i =0; i < currentLoadout.length; i++) {
         
                const chosenSpell = $(`<tr><td class="tref">${currentLoadout[i]}</td></tr>`);
                $("#chosen-spells tbody").append(chosenSpell)
                
            }
        }); 

        //expand the hidden description
        $('.expand-desc').on('click', function() {
            var index = $(this).data('index')
            $('#expanded-view' + index).toggle();
        })
    }

    

    //submit the loadout to backend
    $("#post-loadout").on('click', _ => {
        console.log(currentLoadout)
        $.post('/api/post_loadout', {
            loadout:currentLoadout,
            selected_class:selected_class,
            spell_list_name:spellListName,
            list_desc:listDesc
        })
    })

    this.fetchSpells = () => {
        var fetchedClass = selected_class;
        if (selected_class == 'fighter' || selected_class == 'rogue') {
            fetchedClass = 'Wizard'
        }
        $.get('/api/class_spells', {
            fetchedClass : fetchedClass,
        }, (data) => {
            this.createTable(data);
        })
    }

} 