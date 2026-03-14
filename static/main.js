const api = (path, opts) => fetch(path, opts).then(r => r.json());

// Format number using Indian numbering system (e.g. 1,23,45,678.90)
function formatINR(number){
  const n = Number(number || 0).toFixed(2);
  const [intPart, dec] = n.split('.');
  let i = intPart;
  if(i.length > 3){
    const last3 = i.slice(-3);
    let rest = i.slice(0, -3);
    rest = rest.replace(/\B(?=(\d{2})+(?!\d))/g, ',');
    i = rest + ',' + last3;
  }
  return i + '.' + dec;
}

async function loadProducts(){
  const prods = await api('/api/products');
  const list = document.getElementById('product-list');
  list.innerHTML = '';
  prods.forEach(p => {
    const col = document.createElement('div');
    col.className = 'col-12 col-sm-6 col-md-4 mb-4';
    col.innerHTML = `
      <div class="card product-card h-100">
        <img src="${p.image}" class="card-img-top" alt="${p.name}">
        <div class="card-body d-flex flex-column">
          <h5 class="card-title">${p.name} <span class="badge badge-price ms-2">₹${formatINR(p.price)}</span></h5>
          <p class="card-text text-muted small">${p.description}</p>
          <div class="mt-auto d-flex justify-content-between align-items-center">
            <div class="input-group input-group-sm w-50">
              <input type="number" min="1" value="1" class="form-control qty-input" style="max-width:80px">
            </div>
            <button class="btn btn-success btn-sm add-btn" data-id="${p.id}">Add</button>
          </div>
        </div>
      </div>
    `;
    col.querySelector('.add-btn').addEventListener('click', () => {
      const qty = parseInt(col.querySelector('.qty-input').value || 1, 10);
      addToCart(p.id, qty);
    });
    list.appendChild(col);
  });
}

async function loadCart(){
  const cart = await api('/api/cart');
  const list = document.getElementById('cart-list');
  const navCount = document.getElementById('nav-count');
  list.innerHTML = '';
  let count = 0;
  cart.items.forEach(i => {
    count += i.quantity;
    const el = document.createElement('div');
    el.className = 'list-group-item d-flex justify-content-between align-items-center';
    el.innerHTML = `<div><strong>${i.name}</strong><div class="small text-muted">₹${formatINR(i.price)} &nbsp; qty: <span class="qty">${i.quantity}</span></div></div><div class="btn-group btn-group-sm" role="group"><button class="btn btn-outline-danger remove" data-id="${i.product_id}">-</button><button class="btn btn-outline-secondary addone" data-id="${i.product_id}">+</button></div>`;
    el.querySelector('.remove').addEventListener('click', () => removeFromCart(i.product_id, 1));
    el.querySelector('.addone').addEventListener('click', () => addToCart(i.product_id, 1));
    list.appendChild(el);
  });
  document.getElementById('total').textContent = formatINR(cart.total);
  navCount.textContent = count;
}

async function addToCart(product_id, qty=1){
  await api('/api/cart/add', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({product_id, quantity:qty})});
  await loadCart();
}

async function removeFromCart(product_id, qty=1){
  await api('/api/cart/remove', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({product_id, quantity:qty})});
  await loadCart();
}

async function openCheckoutModal(){
  const res = await api('/api/cart');
  const summary = document.getElementById('order-summary');
  summary.innerHTML = '';
  // show localized current time for preview
  const orderTimeEl = document.getElementById('order-time');
  const now = new Date();
  if(orderTimeEl) orderTimeEl.textContent = 'Order time: ' + new Intl.DateTimeFormat('en-IN', { dateStyle: 'medium', timeStyle: 'short', timeZone: 'Asia/Kolkata' }).format(now);

  res.items.forEach(i => {
    const row = document.createElement('div');
    row.className = 'd-flex justify-content-between mb-2';
    row.innerHTML = `<div>${i.name} x ${i.quantity}</div><div>₹${formatINR(i.price * i.quantity)}</div>`;
    summary.appendChild(row);
  });
  document.getElementById('modal-total').textContent = formatINR(res.total);
  const modalEl = document.getElementById('checkoutModal');
  const modal = new bootstrap.Modal(modalEl);
  modal.show();
}

async function confirmOrder(){
  const res = await api('/api/cart/checkout', {method:'POST'});
  const summary = res.summary || {};
  const confirmedTime = summary.timestamp ? new Intl.DateTimeFormat('en-IN', { dateStyle: 'medium', timeStyle: 'short', timeZone: 'Asia/Kolkata' }).format(new Date(summary.timestamp)) : '';
  alert('Order confirmed! Total: ₹' + formatINR(summary.total) + (confirmedTime ? '\nTime: ' + confirmedTime : ''));
  const modalEl = document.getElementById('checkoutModal');
  const modal = bootstrap.Modal.getInstance(modalEl);
  if(modal) modal.hide();
  await loadCart();
}

document.getElementById('checkout').addEventListener('click', openCheckoutModal);
document.getElementById('confirm-order').addEventListener('click', confirmOrder);

loadProducts();
loadCart();
