$(document).ready(function () {
    const baseURL = 'http://127.0.0.1:5000'

    $('.list-group').on('click', async (e) => {
        e.preventDefault();
        ep = e.target.id
        checkBox = e.target.classList[0]

        let res = await axios.post(`${baseURL}/shows/watch_ep`, {
            userEp: `${ep}`
        })
        if (checkBox === 'far') {
            e.target.classList.toggle('fas')
        }
        if (checkBox === 'fas') {
            e.target.classList.toggle('fas')
        }
    })

    $('.season-list').on('click', async (e) => {
        e.preventDefault();
        season = e.target.id
        checkBox = e.target.classList[0]
        seasonId = season.split(' ')[0]
        seasonEps = $(`.${seasonId}`)
        if (season) {
            let res = await axios.post(`${baseURL}/shows/watch_season`, {
                season: `${season}`
            })
            if (checkBox === 'far') {
                e.target.classList.toggle('fas')
                for (let e of seasonEps) {
                    e.classList.toggle('fas')
                }
            }
            if (checkBox === 'fas') {
                e.target.classList.toggle('far')
                for (let e of seasonEps) {
                    e.classList.toggle('far')
                }
            }
        }

    })

});