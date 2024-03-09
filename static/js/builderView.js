function spellTable(selected_class, spellListName, listDesc) {

    const currentLoadout = [];
    
    this.createTable = (spells) => {
        var activeSpellLevel = spells[0][1];
        $('#spell-container tbody').append(`<tr><td class = "tref"><br><h3 style="font-color:#D27E99;">Level ${activeSpellLevel}<\h3></td>
        <td class = "tref"></td>
        <td class = "tref"></td>
        <td class = "tref"></td>
        <td class = "tref"></td>
        <td class = "tref"></td></tr>`);
        for (let i = 0; i < spells.length; i++){
            const spellRow = $(` 
                <tr>
                    <td class = "tref">
                    <p class = "tref" data-index="${i}" style="cursor: pointer;">${spells[i][0]}</span>
                    <a class="aref expand-desc" data-index="${i}" style="cursor: pointer; font-size:small; font-color:#957FB8;">[see more]</a>
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
                        <span class = "t2 spell-adder" href = "#" data-index = "${i}">+</span>
                    </td>
                </tr>
            `);
            const hiddenDescription = $(`<tr class = "expanded-view" id = "expanded-view${i}" data-index = "${i}" style = "display: none;">
                    <td colspan="6" class = "fulldesc">
                        <br>
                        <h3>${spells[i][0]}</h3>
                        <br>
                        <strong>Level:</strong> ${spells[i][1]}
                        <br><br>
                        <strong> Concentration:</strong> ${spells[i][2] === 1 ? 'Yes' : 'No'}
                        <br><br>
                        <strong>Ritual:</strong> ${spells[i][3] === 1 ? 'Yes' : 'No'}
                        <br><br>
                        <strong>Range:</strong> ${spells[i][4]}
                        <br><br>
                        <strong>Components:</strong> ${spells[i][5]}
                        <br><br>
                        <strong>Duration:</strong> ${spells[i][6]}
                        <br><br>
                        <strong>Casting Time:</strong> ${spells[i][7]}
                        <br><br>
                        <strong>Classes:</strong> ${spells[i][8]}
                        <br><br>
                        <strong>School:</strong> ${spells[i][9]}
                        <br><br>
                        ${spells[i][10]}
                        </td></tr>
            `)
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
            }

            $('.spell-adder').each(function () {
                var buttonIndex = $(this).data('index');
                var buttonText = currentLoadout.includes(spells[buttonIndex][0]) ? '✓' : '+';
                $(this).text(buttonText);
            });

            //adding spells actively into loadout display
            $("#chosen-spells").empty()
            for (let i =0; i < currentLoadout.length; i++) {
         
                const chosenSpell = $(`<div class = "loadout-component">
                                    <div>
                                        <p class = "centered-text" style= "color:#E6C384">${currentLoadout[i]}</p>
                                    </div>
                                    <span class="remove-button" style="color:#E6C384" data-name = "${currentLoadout[i]}">x</span>
                                    </div>`);
                $("#chosen-spells").append(chosenSpell);
    
            }
        }); 

        
        $('.spell-adder').on('mouseenter', function () {
            $(this).css('color', "#7e6b9e");
        }).on('mouseleave', function () {
            $(this).css('color', "#E6C384"); 
        });

        $("#chosen-spells").on('click', '.remove-button', function() {
            var spellName = $(this).data('name');
            var spellIndex = currentLoadout.indexOf(spellName);
            if (spellIndex >= 0) {
                currentLoadout.splice(spellIndex, 1);
            }
            $("#chosen-spells").empty();
            for (let i =0; i < currentLoadout.length; i++) {
        
                const chosenSpell = $(`<div class = "loadout-component">
                                    <div>
                                        <p class = "centered-text" style= "color:#E6C384">${currentLoadout[i]}</p>
                                    </div>
                                    <span class="remove-button" style="color:#E6C384" data-name = "${currentLoadout[i]}">x</span>
                                    </div>`);
                $("#chosen-spells").append(chosenSpell);
            }
        });

        $("#chosen-spells").on({
            mouseenter: function() {
                $(this).css("color", "#7e6b9e");
            },
            mouseleave: function() {
                $(this).css("color", "#E6C384");
            }
        }, '.remove-button');

        //expand the hidden description
        $('.expand-desc').on('click', function() {
            var index = $(this).data('index');
            $('#expanded-view' + index).toggle();
        })




    }


    $('.expand-desc').hover(
        function() {
            $(this).css("color", "#7e6b9e");
        },
        function() {
            $(this).css("color", "#E6C384");
        }
    );

    //submit the loadout to backend
    $("#post-loadout").on('click', _ => {
        $.post('/api/post_loadout', {
            loadout:currentLoadout,
            selected_class:selected_class,
            spell_list_name:spellListName,
            list_desc:listDesc
        })

        document.getElementById("confModal").style.display = "none";
        document.getElementById("overlay").style.display = "none";
        window.location.href = '/'; 
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

