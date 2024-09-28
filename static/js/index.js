const collectionSelect = document.getElementById('collection-select');
const deleteCollectionBtn = document.getElementById('delete-collection-btn');


function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function removeCookie(name) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
}

document.getElementById('add-collection-btn').addEventListener('click', async () => {
    const newCollectionName = document.getElementById('new-collection-name').value;

    if (newCollectionName) {
        try {
            const response = await fetch(`/api/collections/${newCollectionName}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error(`Помилка: ${response.status}`);
            }

            alert('Нова колекція додана успішно!');
            fetchCollectionNames();
        } catch (error) {
            console.error('Помилка додавання колекції:', error);
        }
    } else {
        alert('Введіть назву колекції');
    }
});
async function fetchCollectionData(collectionName) {
    try {
        const response = await fetch(`/api/collections/${collectionName}`);

        if (!response.ok) {
            throw new Error(`Помилка: ${response.status}`);
        }
        const data = await response.json();

        console.log(data)
        const collInfo = document.getElementById('coll-info');
        const collBody = document.getElementById('coll-body');

        collInfo.innerHTML = '';
        collBody.innerHTML = '';

        let headerRow = document.createElement('tr');
        data.fields.forEach(field => {
            let th = document.createElement('th');
            th.textContent = field;
            headerRow.appendChild(th);
        });

        let thUpdate = document.createElement('th');
        thUpdate.textContent = 'Update';
        headerRow.appendChild(thUpdate);

        let thDelete = document.createElement('th');
        thDelete.textContent = 'Delete';
        headerRow.appendChild(thDelete);

        collInfo.appendChild(headerRow);

        data.documents.forEach(doc => {
            let row = document.createElement('tr');

            data.fields.forEach(field => {
                let cell = document.createElement('td');
                let input;

                if (typeof doc[field] === 'string') {
                    if (Date.parse(doc[field])) {
                        input = document.createElement('input');
                        input.type = 'date';
                        input.value = new Date(doc[field]).toISOString().split('T')[0]; // Формат YYYY-MM-DD
                        input.className = 'form-control w-100';
                    } else {
                        input = document.createElement('input');
                        input.type = 'text';
                        input.value = doc[field];
                        input.className = 'form-control w-100';
                    }
                } else if (typeof doc[field] === 'number') {
                    input = document.createElement('input');
                    input.type = 'number';
                    input.value = doc[field];
                    input.className = 'form-control w-100';
                } else if (typeof doc[field] === 'boolean') {
                    input = document.createElement('input');
                    input.type = 'checkbox';
                    input.checked = doc[field];
                } else {
                    input = document.createElement('input');
                    input.type = 'text';
                    input.value = doc[field] ? doc[field].toString() : '';
                    input.className = 'form-control w-100';
                }

                cell.appendChild(input);
                row.appendChild(cell);
            });

            let updateCell = document.createElement('td');
            let updateButton = document.createElement('button');
            updateButton.textContent = 'Update';
            updateButton.classList.add('btn', 'btn-primary');
            updateButton.onclick = () => updateDocument(collectionName, doc._id, row);
            updateCell.appendChild(updateButton);
            row.appendChild(updateCell);

            let deleteCell = document.createElement('td');
            let deleteButton = document.createElement('button');
            deleteButton.textContent = 'Delete';
            deleteButton.classList.add('btn', 'btn-danger');
            deleteButton.onclick = () => deleteDocument(collectionName, doc._id);
            deleteCell.appendChild(deleteButton);
            row.appendChild(deleteCell);

            collBody.appendChild(row);
        });

        let newRow = document.createElement('tr');

        data.fields.forEach(field => {
            let cell = document.createElement('td');
            let input;
            if (typeof data.exampleDocument[field] === 'string') {
                input = document.createElement('input');
                input.type = Date.parse(data.exampleDocument[field]) ? 'date' : 'text';
                input.className = 'form-control w-100';
            } else if (typeof data.exampleDocument[field] === 'number') {
                input = document.createElement('input');
                input.type = 'number';
                input.className = 'form-control w-100';
            } else if (typeof data.exampleDocument[field] === 'boolean') {
                input = document.createElement('input');
                input.type = 'checkbox';
            } else {
                input = document.createElement('input');
                input.type = 'text';
                input.className = 'form-control w-100';
            }

            cell.appendChild(input);
            newRow.appendChild(cell);
        });

        let newButtonCell = document.createElement('td');
        newButtonCell.colSpan = 2;
        let createButton = document.createElement('button');
        createButton.textContent = 'Create';
        createButton.classList.add('btn', 'btn-success');
        createButton.onclick = () => createDocument(collectionName, newRow);
        newButtonCell.appendChild(createButton);
        newRow.appendChild(newButtonCell);

        collBody.appendChild(newRow);
    } catch (error) {
        console.error('Помилка:', error);
    }
}

async function updateDocument(collectionName, docId, row) {
    const inputs = row.querySelectorAll('input');
    let updatedData = {};

    inputs.forEach((input, index) => {
        let fieldName = document.querySelector(`#coll-info th:nth-child(${index + 1})`).textContent;
        if (input.type === 'checkbox') {
            updatedData[fieldName] = input.checked;
        } else if (input.type === 'number') {
            updatedData[fieldName] = parseFloat(input.value);
        } else {
            updatedData[fieldName] = input.value;
        }
    });

    try {
        const response = await fetch(`/api/documents/${collectionName}/${docId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatedData)
        });

        if (!response.ok) {
            throw new Error(`Failed to update document: ${response.status}`);
        }
        alert('Документ оновлено успішно!');
    } catch (error) {
        console.error('Помилка оновлення:', error);
    }
}

async function deleteDocument(collectionName, docId) {
    try {
        const response = await fetch(`/api/documents/${collectionName}/${docId}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error(`Failed to delete document: ${response.status}`);
        }
        alert('Документ видалено успішно!');
        fetchCollectionData(collectionName);
    } catch (error) {
        console.error('Помилка видалення:', error);
    }
}

async function deleteCollection(collectionName) {
    try {
        const response = await fetch(`/api/collections/${collectionName}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error(`Failed to delete collection: ${response.status}`);
        }
        alert('Колекцію видалено успішно!');
        fetchCollectionNames();
    } catch (error) {
        console.error('Помилка видалення колекції:', error);
    }
}

function show_collection() {
    const selectedCollection = collectionSelect.value;
    if (selectedCollection) {
        fetchCollectionData(selectedCollection);
        deleteCollectionBtn.disabled = false;
    } else {
        collInfo.innerHTML = '';
        collBody.innerHTML = '';
        deleteCollectionBtn.disabled = true;
    }
}
collectionSelect.addEventListener('change', function () {
    show_collection();
});

deleteCollectionBtn.addEventListener('click', function () {
    const selectedCollection = collectionSelect.value;
    if (selectedCollection) {
        deleteCollection(selectedCollection);
    }
});
async function fetchCollectionNames() {
    try {
        const response = await fetch('/api/collections');
        if (!response.ok) {
            throw new Error(`Помилка: ${response.status}`);
        }
        const collections = await response.json();

        const collectionSelect = document.getElementById('collection-select');
        collectionSelect.innerHTML = ""

        collections.forEach(collectionName => {
            let option = document.createElement('option');
            option.value = collectionName;
            option.textContent = collectionName;
            collectionSelect.appendChild(option);
        });
        if (collections.length > 0) {
            show_collection();
        }

    } catch (error) {
        console.error('Помилка отримання колекцій:', error);
    }
}

function logoutUser() {
    removeCookie("user")
    checkLoginStatus();
}

function redirectToLogin() {
    window.location.href = '/login';
}

function checkLoginStatus() {
    const username = getCookie('user');
    if (username !== undefined && username !== '') {
        document.getElementById('login-btn').style.display = 'none';
        document.getElementById('logout-btn').style.display = 'inline-block';

    } else {
        document.getElementById('login-btn').style.display = 'inline-block';
        document.getElementById('logout-btn').style.display = 'none';
    }
}
checkLoginStatus();
fetchCollectionNames();