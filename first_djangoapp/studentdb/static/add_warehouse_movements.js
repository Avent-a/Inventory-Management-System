document.addEventListener('DOMContentLoaded', function () {
  var warehouseMinusSelect = document.getElementById('warehouse_minus');
  var componentSelect = document.getElementById('component_name');
  var quantityInput = document.getElementById('quantity');
  var idWarehouseMinusInput = document.getElementById('id_warehouse_minus');
  var errorMessageDiv = document.getElementById('error-message');

  function updateWarehouseDetails() {
  var selectedWarehouseMinusOption = warehouseMinusSelect.options[warehouseMinusSelect.selectedIndex];
  var selectedComponentOption = componentSelect.options[componentSelect.selectedIndex];

  if (selectedWarehouseMinusOption && selectedComponentOption) {
    var warehouseMinusId = selectedWarehouseMinusOption.value;
    var componentId = selectedComponentOption.value;

    console.log('Warehouse Minus ID:', warehouseMinusId);
    console.log('Component ID:', componentId);

    // Use fetch to make a request to the Django view
    fetch(`/calculate-total-quantity/?component_id=${componentId}&warehouse_minus_id=${warehouseMinusId}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        // Update the interface with the received total_quantity value
        updateWarehouseDetailsUI(data.total_quantity, warehouseMinusId);
      })
      .catch(error => {
        console.error('Error fetching total quantity:', error);
      });
  }
}

function updateWarehouseDetailsUI(componentTotalQuantity, warehouseMinusId) {
  if (quantityInput) {
    quantityInput.value = componentTotalQuantity;
    idWarehouseMinusInput.value = warehouseMinusId;  // Устанавливаем IdWarehouseMinus_id в поле формы
  } else {
    console.error('Element Quantity not found.');
  }
}

  function showError(message) {
    if (errorMessageDiv) {
      errorMessageDiv.textContent = message;
    }
  }

  function clearError() {
    showError('');
  }

  if (warehouseMinusSelect && componentSelect && quantityInput && idWarehouseMinusInput) {
    warehouseMinusSelect.addEventListener('change', updateWarehouseDetails);
    componentSelect.addEventListener('change', updateWarehouseDetails);

    updateWarehouseDetails();

    warehouseMinusSelect.addEventListener('change', function () {
      var selectedWarehouseMinusOption = warehouseMinusSelect.options[warehouseMinusSelect.selectedIndex];
      if (selectedWarehouseMinusOption) {
        idWarehouseMinusInput.value = selectedWarehouseMinusOption.value;
      }
    });
  } else {
    console.error('One or more elements not found.');
  }
});

function validateForm() {
  var quantityInput = document.getElementById('quantity');
  var selectedWarehouseMinusSelect = document.getElementById('warehouse_minus');
  var selectedWarehouseMinusOption = selectedWarehouseMinusSelect.options[selectedWarehouseMinusSelect.selectedIndex];
  var selectedComponentSelect = document.getElementById('component_name');
  var selectedComponentOption = componentSelect.options[selectedComponentSelect.selectedIndex];

  console.log('Selected Warehouse Quantity:', selectedWarehouseMinusOption ? selectedWarehouseMinusOption.getAttribute('data-quantity') || selectedWarehouseMinusOption.innerHTML : 'N/A');
  console.log('Selected Component Quantity:', selectedComponentOption ? selectedComponentOption.getAttribute('data-quantity') || selectedComponentOption.innerHTML : 'N/A');

  if (!isPositiveInteger(quantityInput.value)) {
    showError("Quantity must be a positive integer.");
    return false;
  }

  if (selectedWarehouseMinusOption && selectedWarehouseMinusOption.getAttribute('data-quantity') < quantityInput.value) {
    showError("Not enough quantity in the selected warehouse to move.");
    return false;
  }

  if (quantityInput.value < 0) {
    showError("Quantity must be a non-negative value.");
    return false;
  }

  if (!selectedComponentOption) {
    showError("Please select a component.");
    return false;
  }

  clearError();

  return true;
}

function isPositiveInteger(value) {
  return /^\d+$/.test(value) && parseInt(value) > 0;
}

window.onload = function () {
  var currentDate = new Date().toISOString().slice(0, 16);
  document.getElementById("id_date").value = currentDate;
};
