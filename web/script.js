document.addEventListener('DOMContentLoaded', () => {
    const check_input = document.getElementById('check-input');
    const check_btn = document.getElementById('check-btn');

    let commondict = [];
    let technicaldict = [];

    let currentdict = [];

    const dict_switch = document.getElementById('dict-switch');

    check_btn.addEventListener('click', () => {
        const input_value = check_input.value;
        let checkonflag = false;
        commondict.forEach((element, index) => {
            if (element[0] === input_value) {
                current_index = index;
                currentdict = commondict;
                show(currentdict[current_index]);
                dict_switch.checked = false;
                checkonflag = true;
            }
        });
        technicaldict.forEach((element, index) => {
            if (element[0] === input_value) {
                current_index = index;
                currentdict = technicaldict;
                dict_switch.checked = true;
                show(currentdict[current_index]);
                checkonflag = true;
            }
        });
        if (checkonflag == false)
        {
            alert('不在词库当中');
        }
    })    

    

    dict_switch.addEventListener('change', () => {
        if (dict_switch.checked) {
            console.log('checked');
            currentdict = technicaldict;
            current_index = 0;
            show(currentdict[current_index]);
        }
        else {
            console.log('unchecked');
            currentdict = commondict;
            current_index = 0;
            show(currentdict[current_index]);
        }
    })

    fetch('http://localhost:8000/get-common-words')
        .then(response => response.json())
        .then(data => {
            currentdict = commondict = data;
            show(currentdict[0]);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    fetch('http://localhost:8000/get-profess-words')
        .then(response => response.json())
        .then(data => {
            technicaldict = data;
        })
        .catch((error) => {
            console.error('Error:', error);
        });

    const card_title = document.getElementById('card-title');
    const card_title_side = document.getElementById('card-title-side');
    const card_side_up = document.getElementById('card-side-up');
    const card_side_down = document.getElementById('card-side-down');
    const card_body = document.getElementById('card-body');
    const word_parts_list = document.getElementById('word-parts-list');
    const high_freqpair_list = document.getElementById('high-freqpair-list');

    function show(word_list) {
        console.log(word_list);
        word_parts_list.innerHTML = '';
        high_freqpair_list.innerHTML = '';
        let word_list_length = word_list.length;
        if (word_list_length > 1) {
            card_title.innerHTML = word_list[0];
            card_side_up.innerHTML = word_list[1];
            card_side_down.innerHTML = word_list[2];
            num_pair = Number(word_list[3]);
            index_freqpair = num_pair + 4;
            num_freqpair = Number(word_list[index_freqpair]);
            for (let i = 1;i <= num_pair;i++){
                const newLi = document.createElement('li');
                newLi.innerHTML = word_list[3+i];
                word_parts_list.appendChild(newLi);
            }
            for (let j = 1;j <= num_freqpair;j++){
                const newone = document.createElement('li');
                newone.innerHTML = word_list[index_freqpair+j];
                high_freqpair_list.appendChild(newone);
            }
        }
        else {
            card_title.innerHTML = word_list[0];
            card_side_up.innerHTML = 'None';
            card_side_down.innerHTML = 'None';
        }
    }

    const last_btn = document.getElementById('last-btn');
    const next_btn = document.getElementById('next-btn');

    let current_index = 0;

    last_btn.addEventListener('click', () => {
        if (current_index > 0) {
            current_index -= 1;
            show(currentdict[current_index]);
        }
    })

    next_btn.addEventListener('click', () => {
        if (current_index < currentdict.length - 1) {
            current_index += 1;
            show(currentdict[current_index]);
        }
    })
})
