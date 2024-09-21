document.addEventListener('DOMContentLoaded', function() {
    // Sample stock symbols (you should replace this with a complete list or fetch dynamically)
    const stockSymbols = [
        'AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA', 'NFLX', 'FB', 'NVDA', 'DIS', 'BA',
        'IBM', 'INTC', 'AMD', 'ORCL', 'CSCO', 'V', 'MA', 'ADBE', 'CMCSA', 'PFE'
        // Add more stock symbols as needed
    ];
    const datalistElement = document.getElementById('symbol-list');

    // Populate datalist with stock symbols
    stockSymbols.forEach(symbol => {
        const option = document.createElement('option');
        option.value = symbol;
        datalistElement.appendChild(option);
    });
});
