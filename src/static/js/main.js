(function($) {

	"use strict";

	$('nav .dropdown').hover(function(){
		var $this = $(this);
		$this.addClass('show');
		$this.find('> a').attr('aria-expanded', true);
		$this.find('.dropdown-menu').addClass('show');
	}, function(){
		var $this = $(this);
			$this.removeClass('show');
			$this.find('> a').attr('aria-expanded', false);
			$this.find('.dropdown-menu').removeClass('show');
	});

})(jQuery);
const ethereumButton = document.querySelector('.enableEthereumButton');
const sendEthButton = document.querySelector('.sendEthButton');

let accounts = [];

//Sending Ethereum to an address
sendEthButton.addEventListener('click', () => {
  ethereum
    .request({
      method: 'eth_sendTransaction',
      params: [
        {
          from: accounts[0],
          to: '0x2f318C334780961FB129D2a6c30D0763d9a5C970',
          value: '0x29a2241af62c0000',
          gasPrice: '0x09184e72a000',
          gas: '0x2710',
        },
      ],
    })
    .then((txHash) => console.log(txHash))
    .catch((error) => console.error);
});

ethereumButton.addEventListener('click', () => {
  getAccount();
});

async function getAccount() {
  accounts = await ethereum.request({ method: 'eth_requestAccounts' });
}
