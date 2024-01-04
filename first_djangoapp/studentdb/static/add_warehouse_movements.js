document.addEventListener('DOMContentLoaded', function () {
  var warehouseMinusSelect = document.getElementById('warehouse_minus');
  var warehousePlusSelect = document.getElementById('warehouse_plus');
  var componentSelect = document.getElementById('component_name');
  var quantityInput = document.getElementById('quantity');
  var idWarehouseMinusInput = document.getElementById('id_warehouse_minus');
  var errorMessageDiv = document.getElementById('error-message');

  function updateWarehouseDetails() {
    var selectedWarehouseMinusOption = warehouseMinusSelect.options[warehouseMinusSelect.selectedIndex];
    var selectedWarehousePlusOption = warehousePlusSelect.options[warehousePlusSelect.selectedIndex];
    var selectedComponentOption = componentSelect.options[componentSelect.selectedIndex];

    if (selectedWarehouseMinusOption && selectedComponentOption && selectedWarehousePlusOption) {
      var warehouseMinusId = selectedWarehouseMinusOption.value;
      var warehousePlusId = selectedWarehousePlusOption.value;
      var componentId = selectedComponentOption.value;

      console.log('Warehouse Minus ID:', warehouseMinusId);
      console.log('Warehouse Plus ID:', warehousePlusId);
      console.log('Component ID:', componentId);

      // Check if warehouse_minus_id is the same as warehouse_plus_id
      if (warehouseMinusId === warehousePlusId) {
        showError("Warehouse plus and minus cannot be the same.");
        return;
      }

      // Use fetch to make a request to the Django view
      fetch(`/calculate-total-quantity/?component_id=${componentId}&warehouse_minus_id=${warehouseMinusId}&warehouse_plus_id=${warehousePlusId}`)
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

  // Add event listener for changes in the warehouse_plus select element
  if (warehousePlusSelect) {
    warehousePlusSelect.addEventListener('change', updateWarehouseDetails);
  }

  function updateWarehouseDetailsUI(componentTotalQuantity, warehouseMinusId) {
    if (quantityInput) {
      quantityInput.value = componentTotalQuantity;
      idWarehouseMinusInput.value = warehouseMinusId;
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
  var selectedWarehousePlusSelect = document.getElementById('warehouse_plus');
  var selectedWarehousePlusOption = selectedWarehousePlusSelect.options[selectedWarehousePlusSelect.selectedIndex];
  var selectedComponentSelect = document.getElementById('component_name');
  var selectedComponentOption = selectedComponentSelect.options[selectedComponentSelect.selectedIndex];

  console.log('Selected Warehouse Minus ID:', selectedWarehouseMinusOption ? selectedWarehouseMinusOption.value : 'N/A');
  console.log('Selected Warehouse Plus ID:', selectedWarehousePlusOption ? selectedWarehousePlusOption.value : 'N/A');
  console.log('Selected Warehouse Quantity:', selectedWarehouseMinusOption ? selectedWarehouseMinusOption.getAttribute('data-quantity') || selectedWarehouseMinusOption.innerHTML : 'N/A');
  console.log('Selected Component Quantity:', selectedComponentOption ? selectedComponentOption.getAttribute('data-quantity') || selectedComponentOption.innerHTML : 'N/A');

  if (!isPositiveInteger(quantityInput.value)) {
    showError("Quantity must be a positive integer.");
    return false;
  }


  if (!selectedComponentOption) {
    showError("Please select a component.");
    return false;
  }

  // Use strict equality for comparison
  if (selectedWarehouseMinusOption && selectedWarehousePlusOption &&
    selectedWarehouseMinusOption.value === selectedWarehousePlusOption.value) {
    showError("Warehouse plus and minus cannot be the same.");
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
