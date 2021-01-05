console.log('hello world')

const eventBox = document.getElementById('event-box')
console.log(eventBox)

const countdownBox = document.getElementById('countdown-box')
//console.log(eventBox)
const eventDate = Date.parse(eventBox.textContent)
//console.log(evenDate)

setInterval(() => {
    const now = new Date().getTime()
    const diff = eventDate - now
    const d = Math.floor(eventDate/(1000 * 60 * 60 * 24)-(now / ( 1000 * 60 * 60 * 24 )))
    const h = Math.floor((eventDate/(1000 * 60 * 60)-(now / ( 1000 * 60 * 60 ))) % 24 )
    const m = Math.floor((eventDate/(1000 * 60)-(now / ( 1000 * 60 ))) % 60 )
    const s = Math.floor((eventDate/(1000)-(now / ( 1000 ))) % 60 )

    if(diff > 0){
       countdownBox.innerHTML = d + " days, " + h + " hours, " + m + " minutes," + s + " seconds "
    }else{

    }

}, 1000)

