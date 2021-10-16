'use strict';

console.log('ready')

window.addEventListener('load', async () => {

  const data = JSON.parse("{{dash_json|escapejs}}");
  const data_two = JSON.parse("{{cards_json|escapejs}}");
  console.log('data:', data);
  console.log('data:', data_two);

  const TIME = 4000;
  let cards = 0;

  const lotteryCards = document.getElementsByClassName('lottery-cards');
  const refreshIntervalId = setInterval(() => {
    const progressbar = document.querySelector('.progress-contain');
    const firstProgressbar = document.querySelector('.progress-indicator')
    if (firstProgressbar) {
      firstProgressbar.remove();
    }

    const progressIndicator = document.createElement('div');
    progressIndicator.className= 'progress-indicator';
    progressIndicator.style.width = '0%';
    progressbar.appendChild(progressIndicator);

    setTimeout(() => {
      progressIndicator.style.width = '100%';
    }, 10)

    lotteryCards[cards].classList.add('d-block');
    cards++;
    console.log(cards, lotteryCards.length)
    if (cards >= lotteryCards.length) {
      clearInterval(refreshIntervalId);
    }
  }, TIME);
});