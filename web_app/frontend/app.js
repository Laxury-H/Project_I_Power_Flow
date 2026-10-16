/**
 * PowerFlow Studio — Client-side Application Controller
 * Modern Reactive Architecture: Interactive SVG Diagram, Live Data Binding,
 * Real-time Debounced Validation, Y-Bus Matrix Inspector & Newton-Raphson Telemetry.
 */

// Application State
const state = {
  buses: [],
  lines: [],
  baseMva: 100.0,
  displayUnit: 'pu', // 'pu' or 'mw'
  presetId: '3bus',
  validation: { valid: true, errors: [], warnings: [] },
  ybus: null,
  solution: null,
  nodePositions: {}, // { [busId]: { x, y } }
  activeTab: 'tab-split',
  ybusFormat: 'rect' // 'rect' or 'polar'
};

// DOM Cache
const dom = {
  presetSelect: document.getElementById('presetSelect'),
  baseMvaInput: document.getElementById('baseMvaInput'),
  unitToggle: document.getElementById('unitToggle'),
  btnSolve: document.getElementById('btnSolve'),
  btnReset: document.getElementById('btnReset'),
  
  validationBar: document.getElementById('validationBar'),
  valIcon: document.getElementById('valIcon'),
  valStatusText: document.getElementById('valStatusText'),
  valSummary: document.getElementById('valSummary'),
  valAlertList: document.getElementById('valAlertList'),

  busesTableBody: document.getElementById('busesTableBody'),
  linesTableBody: document.getElementById('linesTableBody'),
  busCountBadge: document.getElementById('busCountBadge'),
  lineCountBadge: document.getElementById('lineCountBadge'),
  btnAddBus: document.getElementById('btnAddBus'),
  btnAddLine: document.getElementById('btnAddLine'),
  
  btnImportBusCsv: document.getElementById('btnImportBusCsv'),
  btnExportBusCsv: document.getElementById('btnExportBusCsv'),
  busCsvFileInput: document.getElementById('busCsvFileInput'),
  btnImportLineCsv: document.getElementById('btnImportLineCsv'),
  btnExportLineCsv: document.getElementById('btnExportLineCsv'),
  lineCsvFileInput: document.getElementById('lineCsvFileInput'),

  gridSvg: document.getElementById('gridSvg'),
  layerLines: document.getElementById('layerLines'),
  layerFlowMarkers: document.getElementById('layerFlowMarkers'),
  layerBuses: document.getElementById('layerBuses'),
  btnAutoLayout: document.getElementById('btnAutoLayout'),
  btnZoomIn: document.getElementById('btnZoomIn'),
  btnZoomOut: document.getElementById('btnZoomOut'),
  btnResetView: document.getElementById('btnResetView'),

  ybusTableHead: document.getElementById('ybusTableHead'),
  ybusTableBody: document.getElementById('ybusTableBody'),
  ybusDim: document.getElementById('ybusDim'),
  ybusNonZeros: document.getElementById('ybusNonZeros'),
  ybusSparsity: document.getElementById('ybusSparsity'),
  btnRefreshYbus: document.getElementById('btnRefreshYbus'),

  solverStatusBanner: document.getElementById('solverStatusBanner'),
  solverStatusIcon: document.getElementById('solverStatusIcon'),
  solverStatusTitle: document.getElementById('solverStatusTitle'),
  solverStatusDesc: document.getElementById('solverStatusDesc'),
  kpiGrid: document.getElementById('kpiGrid'),
  convergenceSection: document.getElementById('convergenceSection'),
  busResultsCard: document.getElementById('busResultsCard'),
  branchResultsCard: document.getElementById('branchResultsCard'),
  iterLogTableBody: document.getElementById('iterLogTableBody'),
  iterBadge: document.getElementById('iterBadge'),
  convergenceChart: document.getElementById('convergenceChart'),
  busResultsBody: document.getElementById('busResultsBody'),
  branchResultsBody: document.getElementById('branchResultsBody'),
  btnExportResultsCsv: document.getElementById('btnExportResultsCsv'),

  interactiveTooltip: document.getElementById('interactiveTooltip'),
  toastContainer: document.getElementById('toastContainer')
};

// =============================================================================
// 1. INITIALIZATION & EVENT LISTENERS
// =============================================================================

document.addEventListener('DOMContentLoaded', async () => {
  setupNavigationTabs();
  setupGlobalControls();
  setupDiagramInteractions();
  setupCsvHandling();
  
  // Load default 3-bus benchmark preset
  await loadPreset('3bus');
});

function setupNavigationTabs() {
  const tabs = document.querySelectorAll('.nav-tab');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
      
      tab.classList.add('active');
      const tabId = tab.getAttribute('data-tab');
      document.getElementById(tabId).classList.add('active');
      state.activeTab = tabId;

      if (tabId === 'tab-ybus') {
        fetchAndRenderYbus();
      } else if (tabId === 'tab-diagram') {
        renderDiagram();
      }
    });
  });
}

function setupGlobalControls() {
  dom.presetSelect.addEventListener('change', async (e) => {
    const val = e.target.value;
    if (val !== 'custom') {
      await loadPreset(val);
    }
  });

  dom.baseMvaInput.addEventListener('change', (e) => {
    const val = parseFloat(e.target.value);
    if (!isNaN(val) && val > 0) {
      state.baseMva = val;
      renderTables();
      triggerValidation();
    }
  });

  dom.unitToggle.addEventListener('change', (e) => {
    state.displayUnit = e.target.checked ? 'mw' : 'pu';
    renderTables();
    if (state.solution) {
      renderResults();
    }
  });

  dom.btnSolve.addEventListener('click', runPowerFlowSolve);
  dom.btnReset.addEventListener('click', () => loadPreset(state.presetId));

  dom.btnAddBus.addEventListener('click', () => {
    const nextId = state.buses.length > 0 ? Math.max(...state.buses.map(b => b.bus)) + 1 : 1;
    state.buses.push({
      bus: nextId,
      type: 'PQ',
      pg_pu: 0.0,
      qg_pu: 0.0,
      pd_pu: 0.2,
      qd_pu: 0.1,
      vm_pu: 1.0,
      va_deg: 0.0,
      q_min_pu: 0.0,
      q_max_pu: 0.0
    });
    calculateNodePositions();
    renderTables();
    renderDiagram();
    triggerValidation();
  });

  dom.btnAddLine.addEventListener('click', () => {
    if (state.buses.length < 2) {
      showToast('Cần ít nhất 2 nút để tạo đường dây!', 'error');
      return;
    }
    const fb = state.buses[0].bus;
    const tb = state.buses[1].bus;
    state.lines.push({
      from_bus: fb,
      to_bus: tb,
      r_pu: 0.05,
      x_pu: 0.15
    });
    renderTables();
    renderDiagram();
    triggerValidation();
  });

  dom.btnRefreshYbus.addEventListener('click', fetchAndRenderYbus);
  
  document.querySelectorAll('input[name="ybusFormat"]').forEach(r => {
    r.addEventListener('change', (e) => {
      state.ybusFormat = e.target.value;
      if (state.ybus) renderYbusTable(state.ybus);
    });
  });

  dom.btnExportResultsCsv.addEventListener('click', exportResultsToCsv);
}


// =============================================================================
// 2. PRESETS & DATA BINDING
// =============================================================================

async function loadPreset(presetId) {
  try {
    const res = await fetch(`/api/presets/${presetId}`);
    if (!res.ok) throw new Error('Không thể tải kịch bản');
    const data = await res.json();
    
    state.presetId = presetId;
    state.buses = JSON.parse(JSON.stringify(data.buses));
    state.lines = JSON.parse(JSON.stringify(data.lines));
    state.baseMva = data.base_mva || 100.0;
    dom.baseMvaInput.value = state.baseMva;
    dom.presetSelect.value = presetId;
    state.solution = null;

    calculateNodePositions();
    renderTables();
    renderDiagram();
    triggerValidation();
    resetResultsView();

    showToast(`Đã nạp ${data.name} thành công!`, 'success');
  } catch (err) {
    showToast(`Lỗi nạp kịch bản: ${err.message}`, 'error');
  }
}

function calculateNodePositions() {
  const n = state.buses.length;
  if (n === 0) return;
  const cx = 400;
  const cy = 300;
  const radius = Math.min(260, 80 + n * 30);

  state.buses.forEach((b, i) => {
    if (!state.nodePositions[b.bus]) {
      const angle = (2 * Math.PI * i) / n - Math.PI / 2;
      state.nodePositions[b.bus] = {
        x: cx + radius * Math.cos(angle),
        y: cy + radius * Math.sin(angle)
      };
    }
  });
}

function resetResultsView() {
  dom.solverStatusBanner.className = 'solver-status-banner info';
  dom.solverStatusIcon.textContent = 'ℹ';
  dom.solverStatusTitle.textContent = 'Chưa thực hiện tính toán';
  dom.solverStatusDesc.innerHTML = 'Nhấn nút <strong>"Giải trào lưu"</strong> ở góc trên bên phải để bắt đầu thuật toán Newton-Raphson.';
  
  dom.kpiGrid.style.display = 'none';
  dom.convergenceSection.style.display = 'none';
  dom.busResultsCard.style.display = 'none';
  dom.branchResultsCard.style.display = 'none';
}


// =============================================================================
// 3. TABLE RENDERING & INLINE EDITING
// =============================================================================

function renderTables() {
  dom.busCountBadge.textContent = `${state.buses.length} nút`;
  dom.lineCountBadge.textContent = `${state.lines.length} đường dây`;

  const isMw = state.displayUnit === 'mw';
  const factor = isMw ? state.baseMva : 1.0;

  // Render Buses Table
  dom.busesTableBody.innerHTML = '';
  state.buses.forEach((b, idx) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${b.bus}</strong></td>
      <td>
        <select class="select-cell" data-idx="${idx}" data-field="type">
          <option value="Slack" ${b.type === 'Slack' ? 'selected' : ''}>Slack</option>
          <option value="PV" ${b.type === 'PV' ? 'selected' : ''}>PV</option>
          <option value="PQ" ${b.type === 'PQ' ? 'selected' : ''}>PQ</option>
        </select>
      </td>
      <td><input type="number" step="any" class="editable-cell" data-idx="${idx}" data-field="pg_pu" value="${formatNum(b.pg_pu * factor)}"></td>
      <td><input type="number" step="any" class="editable-cell" data-idx="${idx}" data-field="qg_pu" value="${formatNum(b.qg_pu * factor)}"></td>
      <td><input type="number" step="any" class="editable-cell" data-idx="${idx}" data-field="pd_pu" value="${formatNum(b.pd_pu * factor)}"></td>
      <td><input type="number" step="any" class="editable-cell" data-idx="${idx}" data-field="qd_pu" value="${formatNum(b.qd_pu * factor)}"></td>
      <td><input type="number" step="0.01" class="editable-cell" data-idx="${idx}" data-field="vm_pu" value="${b.vm_pu}"></td>
      <td><input type="number" step="0.5" class="editable-cell" data-idx="${idx}" data-field="va_deg" value="${b.va_deg}"></td>
      <td><input type="number" step="any" class="editable-cell" data-idx="${idx}" data-field="q_min_pu" value="${b.q_min_pu !== undefined ? formatNum(b.q_min_pu * factor) : ''}" placeholder="-"></td>
      <td><input type="number" step="any" class="editable-cell" data-idx="${idx}" data-field="q_max_pu" value="${b.q_max_pu !== undefined ? formatNum(b.q_max_pu * factor) : ''}" placeholder="-"></td>
      <td><button class="btn-del-row" data-idx="${idx}" title="Xóa nút này">✕</button></td>
    `;
    dom.busesTableBody.appendChild(tr);
  });

  // Render Lines Table
  dom.linesTableBody.innerHTML = '';
  state.lines.forEach((l, idx) => {
    const zMag = Math.sqrt(l.r_pu * l.r_pu + l.x_pu * l.x_pu);
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><input type="number" class="editable-cell" data-line-idx="${idx}" data-field="from_bus" value="${l.from_bus}"></td>
      <td><input type="number" class="editable-cell" data-line-idx="${idx}" data-field="to_bus" value="${l.to_bus}"></td>
      <td><input type="number" step="0.001" class="editable-cell" data-line-idx="${idx}" data-field="r_pu" value="${l.r_pu}"></td>
      <td><input type="number" step="0.001" class="editable-cell" data-line-idx="${idx}" data-field="x_pu" value="${l.x_pu}"></td>
      <td><span class="font-mono text-muted">${zMag.toFixed(4)}</span></td>
      <td><button class="btn-del-line-row" data-line-idx="${idx}" title="Xóa đường dây">✕</button></td>
    `;
    dom.linesTableBody.appendChild(tr);
  });

  attachTableEventListeners();
}

function attachTableEventListeners() {
  // Bus input change
  dom.busesTableBody.querySelectorAll('.editable-cell, .select-cell').forEach(elem => {
    elem.addEventListener('change', (e) => {
      const idx = parseInt(e.target.getAttribute('data-idx'));
      const field = e.target.getAttribute('data-field');
      let val = e.target.value;

      if (field === 'type') {
        state.buses[idx].type = val;
      } else {
        const numVal = parseFloat(val);
        const factor = state.displayUnit === 'mw' ? (1.0 / state.baseMva) : 1.0;
        if (field.endsWith('_pu')) {
          state.buses[idx][field] = isNaN(numVal) ? 0.0 : numVal * factor;
        } else {
          state.buses[idx][field] = isNaN(numVal) ? 0.0 : numVal;
        }
      }

      markCustomPreset();
      renderDiagram();
      triggerValidation();
    });
  });

  // Delete bus button
  dom.busesTableBody.querySelectorAll('.btn-del-row').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const idx = parseInt(e.target.getAttribute('data-idx'));
      const deletedBusId = state.buses[idx].bus;
      state.buses.splice(idx, 1);
      // Remove connected lines
      state.lines = state.lines.filter(l => l.from_bus !== deletedBusId && l.to_bus !== deletedBusId);
      delete state.nodePositions[deletedBusId];

      markCustomPreset();
      renderTables();
      renderDiagram();
      triggerValidation();
    });
  });

  // Line input change
  dom.linesTableBody.querySelectorAll('.editable-cell').forEach(elem => {
    elem.addEventListener('change', (e) => {
      const idx = parseInt(e.target.getAttribute('data-line-idx'));
      const field = e.target.getAttribute('data-field');
      const val = parseFloat(e.target.value);
      state.lines[idx][field] = isNaN(val) ? 0.0 : val;

      markCustomPreset();
      renderTables();
      renderDiagram();
      triggerValidation();
    });
  });

  // Delete line button
  dom.linesTableBody.querySelectorAll('.btn-del-line-row').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const idx = parseInt(e.target.getAttribute('data-line-idx'));
      state.lines.splice(idx, 1);
      markCustomPreset();
      renderTables();
      renderDiagram();
      triggerValidation();
    });
  });
}

function markCustomPreset() {
  dom.presetSelect.value = 'custom';
  state.presetId = 'custom';
}


// =============================================================================
// 4. REAL-TIME DEBOUNCED VALIDATION
// =============================================================================

let validationTimeout = null;
function triggerValidation() {
  clearTimeout(validationTimeout);
  validationTimeout = setTimeout(performLiveValidation, 250);
}

async function performLiveValidation() {
  try {
    const res = await fetch('/api/validate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        buses: state.buses,
        lines: state.lines,
        base_mva: state.baseMva
      })
    });

    const data = await res.json();
    state.validation = data;

    if (data.valid) {
      dom.validationBar.className = 'validation-bar valid';
      dom.valIcon.textContent = '✓';
      dom.valStatusText.textContent = 'Dữ liệu hoàn toàn hợp lệ';
      dom.valSummary.textContent = `${data.slack_count} nút Slack • ${data.pv_count} nút PV • ${data.pq_count} nút PQ • ${data.line_count} đường dây liên thông`;
      dom.valAlertList.style.display = 'none';
      dom.btnSolve.disabled = false;
    } else {
      dom.validationBar.className = 'validation-bar invalid';
      dom.valIcon.textContent = '✕';
      dom.valStatusText.textContent = `Phát hiện ${data.errors.length} lỗi trong dữ liệu đầu vào:`;
      dom.valSummary.textContent = 'Vui lòng sửa các lỗi bên dưới trước khi giải trào lưu.';
      
      dom.valAlertList.innerHTML = data.errors.map(err => `<div class="val-alert-item">${err}</div>`).join('');
      dom.valAlertList.style.display = 'flex';
      dom.btnSolve.disabled = true;
    }
  } catch (err) {
    console.error('Validation API error:', err);
  }
}


// =============================================================================
// 5. INTERACTIVE SVG DIAGRAM ENGINE
// =============================================================================

let isDragging = false;
let draggedBusId = null;
let dragOffset = { x: 0, y: 0 };

function setupDiagramInteractions() {
  dom.btnAutoLayout.addEventListener('click', () => {
    state.nodePositions = {};
    calculateNodePositions();
    renderDiagram();
    showToast('Đã sắp xếp lại bố cục sơ đồ!', 'info');
  });

  dom.btnResetView.addEventListener('click', () => {
    dom.gridSvg.setAttribute('viewBox', '0 0 800 600');
  });

  // SVG Drag & Drop
  dom.gridSvg.addEventListener('mousedown', (e) => {
    const busGroup = e.target.closest('.svg-bus-group');
    if (busGroup) {
      isDragging = true;
      draggedBusId = parseInt(busGroup.getAttribute('data-bus-id'));
      const pt = getSvgCursorPoint(e);
      dragOffset.x = pt.x - state.nodePositions[draggedBusId].x;
      dragOffset.y = pt.y - state.nodePositions[draggedBusId].y;
    }
  });

  window.addEventListener('mousemove', (e) => {
    if (isDragging && draggedBusId !== null) {
      const pt = getSvgCursorPoint(e);
      state.nodePositions[draggedBusId].x = Math.max(30, Math.min(770, pt.x - dragOffset.x));
      state.nodePositions[draggedBusId].y = Math.max(30, Math.min(570, pt.y - dragOffset.y));
      renderDiagram();
    }
  });

  window.addEventListener('mouseup', () => {
    isDragging = false;
    draggedBusId = null;
  });
}

function getSvgCursorPoint(e) {
  const pt = dom.gridSvg.createSVGPoint();
  pt.x = e.clientX;
  pt.y = e.clientY;
  return pt.matrixTransform(dom.gridSvg.getScreenCTM().inverse());
}

function renderDiagram() {
  dom.layerLines.innerHTML = '';
  dom.layerFlowMarkers.innerHTML = '';
  dom.layerBuses.innerHTML = '';

  const busMap = {};
  state.buses.forEach(b => { busMap[b.bus] = b; });

  // Draw Lines
  state.lines.forEach((line, idx) => {
    const posA = state.nodePositions[line.from_bus];
    const posB = state.nodePositions[line.to_bus];
    if (!posA || !posB) return;

    const gLine = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    path.setAttribute('x1', posA.x);
    path.setAttribute('y1', posA.y);
    path.setAttribute('x2', posB.x);
    path.setAttribute('y2', posB.y);
    path.setAttribute('class', 'svg-line');
    path.setAttribute('data-line-idx', idx);

    // If solved, show flow direction & power
    let branchSol = null;
    if (state.solution && state.solution.branches) {
      branchSol = state.solution.branches.find(b => b.from_bus === line.from_bus && b.to_bus === line.to_bus);
    }

    if (branchSol) {
      path.classList.add('svg-line-flow');
      // Flow arrow mid point
      const midX = (posA.x + posB.x) / 2;
      const midY = (posA.y + posB.y) / 2;
      const textFlow = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      textFlow.setAttribute('x', midX);
      textFlow.setAttribute('y', midY - 8);
      textFlow.setAttribute('class', 'svg-bus-label');
      textFlow.textContent = `${branchSol.p_from_MW.toFixed(1)} MW (ΔP: ${branchSol.p_loss_MW.toFixed(2)})`;
      dom.layerFlowMarkers.appendChild(textFlow);
    }

    // Line tooltip
    path.addEventListener('mouseenter', (e) => {
      let content = `<div class="tooltip-title">Đường dây ${line.from_bus} ➜ ${line.to_bus}</div>`;
      content += `<div class="tooltip-row"><span class="tooltip-label">R / X:</span> <span>${line.r_pu} / ${line.x_pu} pu</span></div>`;
      if (branchSol) {
        content += `<div class="tooltip-row"><span class="tooltip-label">P đầu gửi:</span> <span>${branchSol.p_from_MW} MW</span></div>`;
        content += `<div class="tooltip-row"><span class="tooltip-label">Q đầu gửi:</span> <span>${branchSol.q_from_Mvar} Mvar</span></div>`;
        content += `<div class="tooltip-row"><span class="tooltip-label">Tổn thất ΔP:</span> <span class="text-danger font-bold">${branchSol.p_loss_MW} MW</span></div>`;
        content += `<div class="tooltip-row"><span class="tooltip-label">Tổn thất ΔQ:</span> <span>${branchSol.q_loss_Mvar} Mvar</span></div>`;
        content += `<div class="tooltip-row"><span class="tooltip-label">Dòng điện |I|:</span> <span>${branchSol.current_pu} pu</span></div>`;
      }
      showTooltip(e, content);
    });
    path.addEventListener('mouseleave', hideTooltip);

    gLine.appendChild(path);
    dom.layerLines.appendChild(gLine);
  });

  // Draw Buses
  state.buses.forEach(b => {
    const pos = state.nodePositions[b.bus];
    if (!pos) return;

    const gBus = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    gBus.setAttribute('class', 'svg-bus-group');
    gBus.setAttribute('data-bus-id', b.bus);
    gBus.setAttribute('transform', `translate(${pos.x}, ${pos.y})`);

    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('r', 22);
    circle.setAttribute('class', 'svg-bus-circle');
    
    let strokeCol = '#06B6D4';
    let fillCol = 'rgba(6, 182, 212, 0.25)';
    if (b.type === 'Slack') {
      strokeCol = '#EC4899';
      fillCol = 'rgba(236, 72, 153, 0.3)';
    } else if (b.type === 'PV') {
      strokeCol = '#F59E0B';
      fillCol = 'rgba(245, 158, 11, 0.3)';
    }

    circle.setAttribute('stroke', strokeCol);
    circle.setAttribute('fill', fillCol);

    const textId = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    textId.setAttribute('class', 'svg-bus-text');
    textId.textContent = b.bus;

    const textLabel = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    textLabel.setAttribute('y', 36);
    textLabel.setAttribute('class', 'svg-bus-label');

    // Display solved voltage if available
    let busSol = null;
    if (state.solution && state.solution.buses) {
      busSol = state.solution.buses.find(item => item.bus === b.bus);
    }
    
    if (busSol) {
      textLabel.textContent = `${busSol.vm_pu.toFixed(3)}∠${busSol.va_deg.toFixed(1)}°`;
    } else {
      textLabel.textContent = `${b.type} (${b.vm_pu} pu)`;
    }

    gBus.appendChild(circle);
    gBus.appendChild(textId);
    gBus.appendChild(textLabel);

    // Hover Tooltip
    gBus.addEventListener('mouseenter', (e) => {
      let content = `<div class="tooltip-title">Thanh cái Bus ${b.bus} [${b.type}]</div>`;
      if (busSol) {
        content += `<div class="tooltip-row"><span class="tooltip-label">Điện áp |V|:</span> <span class="font-bold text-primary">${busSol.vm_pu} pu</span></div>`;
        content += `<div class="tooltip-row"><span class="tooltip-label">Góc pha δ:</span> <span>${busSol.va_deg}° (${busSol.va_rad} rad)</span></div>`;
        content += `<div class="tooltip-row"><span class="tooltip-label">P phát:</span> <span>${busSol.pg_MW} MW</span></div>`;
        content += `<div class="tooltip-row"><span class="tooltip-label">Q phát:</span> <span>${busSol.qg_Mvar} Mvar</span></div>`;
        content += `<div class="tooltip-row"><span class="tooltip-label">P tải:</span> <span>${busSol.pd_MW} MW</span></div>`;
        content += `<div class="tooltip-row"><span class="tooltip-label">Q tải:</span> <span>${busSol.qd_Mvar} Mvar</span></div>`;
        content += `<div class="tooltip-row"><span class="tooltip-label">Trạng thái Q:</span> <span>${busSol.q_status}</span></div>`;
      } else {
        content += `<div class="tooltip-row"><span class="tooltip-label">Điện áp đặt:</span> <span>${b.vm_pu} pu</span></div>`;
        content += `<div class="tooltip-row"><span class="tooltip-label">Góc ban đầu:</span> <span>${b.va_deg}°</span></div>`;
        content += `<div class="tooltip-row"><span class="tooltip-label">P tải:</span> <span>${(b.pd_pu * state.baseMva).toFixed(1)} MW</span></div>`;
        content += `<div class="tooltip-row"><span class="tooltip-label">Q tải:</span> <span>${(b.qd_pu * state.baseMva).toFixed(1)} Mvar</span></div>`;
      }
      showTooltip(e, content);
    });
    gBus.addEventListener('mouseleave', hideTooltip);

    dom.layerBuses.appendChild(gBus);
  });
}

function showTooltip(e, htmlContent) {
  dom.interactiveTooltip.innerHTML = htmlContent;
  dom.interactiveTooltip.style.display = 'block';
  positionTooltip(e);
}

function positionTooltip(e) {
  const x = e.clientX + 16;
  const y = e.clientY + 16;
  dom.interactiveTooltip.style.left = `${Math.min(window.innerWidth - 240, x)}px`;
  dom.interactiveTooltip.style.top = `${Math.min(window.innerHeight - 200, y)}px`;
}

function hideTooltip() {
  dom.interactiveTooltip.style.display = 'none';
}


// =============================================================================
// 6. Y-BUS MATRIX INSPECTOR
// =============================================================================

async function fetchAndRenderYbus() {
  try {
    const res = await fetch('/api/build-ybus', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        buses: state.buses,
        lines: state.lines,
        base_mva: state.baseMva
      })
    });
    if (!res.ok) throw new Error('Không thể lập ma trận Y-bus');
    const data = await res.json();
    state.ybus = data;

    dom.ybusDim.textContent = `${data.dim} × ${data.dim}`;
    dom.ybusNonZeros.textContent = data.non_zeros;
    dom.ybusSparsity.textContent = `${data.sparsity} %`;

    renderYbusTable(data);
  } catch (err) {
    showToast(`Lỗi Y-bus: ${err.message}`, 'error');
  }
}

function renderYbusTable(ybusData) {
  const { bus_ids, matrix, dim } = ybusData;
  const isPolar = state.ybusFormat === 'polar';

  // Build Table Head
  let theadHtml = '<tr><th>Bus</th>';
  bus_ids.forEach(id => {
    theadHtml += `<th>Bus ${id}</th>`;
  });
  theadHtml += '</tr>';
  dom.ybusTableHead.innerHTML = theadHtml;

  // Build Table Body
  let tbodyHtml = '';
  for (let i = 0; i < dim; i++) {
    tbodyHtml += `<tr><th><strong>Bus ${bus_ids[i]}</strong></th>`;
    for (let j = 0; j < dim; j++) {
      const cell = matrix[i][j];
      const isDiag = cell.is_diagonal ? 'diagonal' : '';
      let displayStr = '';

      if (isPolar) {
        displayStr = `${cell.magnitude.toFixed(3)} ∠ ${cell.angle_deg.toFixed(1)}°`;
      } else {
        const sign = cell.b >= 0 ? '+' : '-';
        displayStr = `${cell.g.toFixed(3)} ${sign} j${Math.abs(cell.b).toFixed(3)}`;
      }

      tbodyHtml += `<td class="${isDiag}" title="Y[${bus_ids[i]}, ${bus_ids[j]}] = ${displayStr}">${displayStr}</td>`;
    }
    tbodyHtml += '</tr>';
  }
  dom.ybusTableBody.innerHTML = tbodyHtml;
}


// =============================================================================
// 7. NEWTON-RAPHSON SOLVER EXECUTION & RESULTS PRESENTATION
// =============================================================================

async function runPowerFlowSolve() {
  dom.btnSolve.classList.add('loading');
  dom.btnSolve.disabled = true;

  try {
    const res = await fetch('/api/solve', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        buses: state.buses,
        lines: state.lines,
        base_mva: state.baseMva,
        tolerance: 1e-6,
        max_iterations: 30
      })
    });

    const solution = await res.json();
    state.solution = solution;

    if (solution.converged) {
      showToast(`Thuật toán hội tụ thành công sau ${solution.iterations} vòng lặp!`, 'success');
      dom.solverStatusBanner.className = 'solver-status-banner success';
      dom.solverStatusIcon.textContent = '✓';
      dom.solverStatusTitle.textContent = `Hội tụ thành công (${solution.iterations} vòng lặp)`;
      dom.solverStatusDesc.textContent = solution.message;
    } else {
      showToast(`Không thể hội tụ: ${solution.message}`, 'error');
      dom.solverStatusBanner.className = 'solver-status-banner error';
      dom.solverStatusIcon.textContent = '✕';
      dom.solverStatusTitle.textContent = 'Thuật toán không hội tụ';
      dom.solverStatusDesc.textContent = solution.message;
    }

    renderResults();
    renderDiagram(); // update diagram with solved voltages and flow arrows

    // Automatically switch to Results Tab
    document.querySelector('.nav-tab[data-tab="tab-results"]').click();
  } catch (err) {
    showToast(`Lỗi giải trào lưu: ${err.message}`, 'error');
  } finally {
    dom.btnSolve.classList.remove('loading');
    dom.btnSolve.disabled = false;
  }
}

function renderResults() {
  const sol = state.solution;
  if (!sol) return;

  // Render KPI Metrics
  if (sol.summary && sol.converged) {
    dom.kpiGrid.style.display = 'grid';
    document.getElementById('kpiGenP').textContent = `${sol.summary.total_generation_MW.toFixed(2)} MW`;
    document.getElementById('kpiGenQ').textContent = `${sol.summary.total_generation_Mvar.toFixed(2)} Mvar`;
    document.getElementById('kpiLoadP').textContent = `${sol.summary.total_demand_MW.toFixed(2)} MW`;
    document.getElementById('kpiLoadQ').textContent = `${sol.summary.total_demand_Mvar.toFixed(2)} Mvar`;
    document.getElementById('kpiLossP').textContent = `${sol.summary.total_loss_MW.toFixed(4)} MW`;
    document.getElementById('kpiLossPct').textContent = `(${sol.summary.loss_percentage}% tổng phát)`;
    
    const balErr = sol.summary.p_balance_error_MW;
    document.getElementById('kpiBalanceError').textContent = balErr < 1e-10 ? '< 10⁻¹² MW' : `${balErr.toExponential(3)} MW`;
  }

  // Render Convergence Table & Chart
  if (sol.history && sol.history.length > 0) {
    dom.convergenceSection.style.display = 'grid';
    dom.iterBadge.textContent = `${sol.history.length - 1} vòng lặp`;
    
    dom.iterLogTableBody.innerHTML = sol.history.map(h => `
      <tr>
        <td><strong>#${h.iteration}</strong></td>
        <td class="font-mono">${h.max_p_mismatch_pu.toExponential(4)}</td>
        <td class="font-mono">${h.max_q_mismatch_pu.toExponential(4)}</td>
        <td class="font-mono font-bold text-primary">${h.max_mismatch_pu.toExponential(4)}</td>
        <td>${h.iteration === sol.iterations && sol.converged ? '<span class="bus-badge badge-status-ok">Hội tụ</span>' : '<span class="text-muted">Đang lặp...</span>'}</td>
      </tr>
    `).join('');

    drawConvergenceChart(sol.history);
  }

  // Render Bus Results Table
  if (sol.buses && sol.buses.length > 0) {
    dom.busResultsCard.style.display = 'block';
    dom.busResultsBody.innerHTML = sol.buses.map(b => {
      const qStatusClass = b.q_status === 'OK' ? 'badge-status-ok' : 'badge-status-warn';
      return `
        <tr>
          <td><strong>${b.bus}</strong></td>
          <td><span class="bus-badge badge-${b.type.toLowerCase()}">${b.type}</span></td>
          <td class="font-mono font-bold text-primary">${b.vm_pu.toFixed(4)}</td>
          <td class="font-mono">${b.va_deg.toFixed(2)}°</td>
          <td class="font-mono">${b.p_net_MW.toFixed(2)}</td>
          <td class="font-mono">${b.q_net_Mvar.toFixed(2)}</td>
          <td class="font-mono">${b.pg_MW.toFixed(2)}</td>
          <td class="font-mono">${b.qg_Mvar.toFixed(2)}</td>
          <td class="font-mono">${b.pd_MW.toFixed(2)}</td>
          <td class="font-mono">${b.qd_Mvar.toFixed(2)}</td>
          <td><span class="bus-badge ${qStatusClass}">${b.q_status}</span></td>
        </tr>
      `;
    }).join('');
  }

  // Render Branch Results Table
  if (sol.branches && sol.branches.length > 0) {
    dom.branchResultsCard.style.display = 'block';
    dom.branchResultsBody.innerHTML = sol.branches.map(br => `
      <tr>
        <td><strong>Bus ${br.from_bus}</strong></td>
        <td><strong>Bus ${br.to_bus}</strong></td>
        <td class="font-mono">${br.p_from_MW.toFixed(2)}</td>
        <td class="font-mono">${br.q_from_Mvar.toFixed(2)}</td>
        <td class="font-mono">${br.p_to_MW.toFixed(2)}</td>
        <td class="font-mono">${br.q_to_Mvar.toFixed(2)}</td>
        <td class="font-mono font-bold text-danger">${br.p_loss_MW.toFixed(4)}</td>
        <td class="font-mono">${br.q_loss_Mvar.toFixed(4)}</td>
        <td class="font-mono">${br.i2r_MW.toFixed(4)}</td>
        <td class="font-mono">${br.current_pu.toFixed(4)}</td>
      </tr>
    `).join('');
  }
}

function drawConvergenceChart(history) {
  const canvas = dom.convergenceChart;
  const ctx = canvas.getContext('2d');
  const w = canvas.width;
  const h = canvas.height;

  ctx.clearRect(0, 0, w, h);

  const padLeft = 45;
  const padBottom = 30;
  const padTop = 20;
  const padRight = 20;

  const chartW = w - padLeft - padRight;
  const chartH = h - padTop - padBottom;

  const n = history.length;
  if (n < 2) return;

  const logs = history.map(h => h.log10_mismatch);
  const minLog = Math.min(-16, Math.min(...logs));
  const maxLog = Math.max(1, Math.max(...logs));

  // Draw Grid Lines
  ctx.strokeStyle = '#1E293B';
  ctx.lineWidth = 1;
  ctx.fillStyle = '#64748B';
  ctx.font = '10px JetBrains Mono';

  for (let l = Math.ceil(minLog); l <= Math.floor(maxLog); l += 4) {
    const y = padTop + chartH * (1 - (l - minLog) / (maxLog - minLog));
    ctx.beginPath();
    ctx.moveTo(padLeft, y);
    ctx.lineTo(w - padRight, y);
    ctx.stroke();
    ctx.fillText(`10^${l}`, 6, y + 3);
  }

  // Draw Line Trajectory
  ctx.strokeStyle = '#38BDF8';
  ctx.lineWidth = 2.5;
  ctx.beginPath();

  history.forEach((pt, i) => {
    const x = padLeft + (i / (n - 1)) * chartW;
    const y = padTop + chartH * (1 - (pt.log10_mismatch - minLog) / (maxLog - minLog));
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.stroke();

  // Draw Data Points
  history.forEach((pt, i) => {
    const x = padLeft + (i / (n - 1)) * chartW;
    const y = padTop + chartH * (1 - (pt.log10_mismatch - minLog) / (maxLog - minLog));

    ctx.fillStyle = '#0284C7';
    ctx.beginPath();
    ctx.arc(x, y, 4, 0, 2 * Math.PI);
    ctx.fill();

    ctx.fillStyle = '#94A3B8';
    ctx.fillText(`#${pt.iteration}`, x - 6, h - 10);
  });
}


// =============================================================================
// 8. CSV IMPORT & EXPORT UTILITIES
// =============================================================================

function setupCsvHandling() {
  // Bus Import
  dom.btnImportBusCsv.addEventListener('click', () => dom.busCsvFileInput.click());
  dom.busCsvFileInput.addEventListener('change', (e) => handleCsvUpload(e, 'buses'));

  // Line Import
  dom.btnImportLineCsv.addEventListener('click', () => dom.lineCsvFileInput.click());
  dom.lineCsvFileInput.addEventListener('change', (e) => handleCsvUpload(e, 'lines'));

  // Bus Export
  dom.btnExportBusCsv.addEventListener('click', () => {
    exportToCsv(state.buses, 'buses_input.csv');
  });

  // Line Export
  dom.btnExportLineCsv.addEventListener('click', () => {
    exportToCsv(state.lines, 'lines_input.csv');
  });
}

function handleCsvUpload(e, targetType) {
  const file = e.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (event) => {
    try {
      const text = event.target.result;
      const rows = parseCsvText(text);
      if (rows.length === 0) throw new Error('Tệp CSV trống');

      if (targetType === 'buses') {
        state.buses = rows.map(r => ({
          bus: parseInt(r.bus),
          type: r.type,
          pg_pu: parseFloat(r.pg_pu || 0),
          qg_pu: parseFloat(r.qg_pu || 0),
          pd_pu: parseFloat(r.pd_pu || 0),
          qd_pu: parseFloat(r.qd_pu || 0),
          vm_pu: parseFloat(r.vm_pu || 1.0),
          va_deg: parseFloat(r.va_deg || 0.0),
          q_min_pu: r.q_min_pu ? parseFloat(r.q_min_pu) : undefined,
          q_max_pu: r.q_max_pu ? parseFloat(r.q_max_pu) : undefined
        }));
      } else {
        state.lines = rows.map(r => ({
          from_bus: parseInt(r.from_bus),
          to_bus: parseInt(r.to_bus),
          r_pu: parseFloat(r.r_pu || 0),
          x_pu: parseFloat(r.x_pu || 0)
        }));
      }

      markCustomPreset();
      calculateNodePositions();
      renderTables();
      renderDiagram();
      triggerValidation();
      showToast(`Đã nhập thành công ${rows.length} hàng dữ liệu ${targetType}!`, 'success');
    } catch (err) {
      showToast(`Lỗi đọc CSV: ${err.message}`, 'error');
    }
  };
  reader.readAsText(file);
}

function parseCsvText(csvText) {
  const lines = csvText.trim().split(/\r\n|\n/);
  if (lines.length < 2) return [];
  const headers = lines[0].split(',').map(h => h.trim());
  const result = [];

  for (let i = 1; i < lines.length; i++) {
    if (!lines[i].trim()) continue;
    const values = lines[i].split(',').map(v => v.trim());
    const obj = {};
    headers.forEach((h, idx) => {
      obj[h] = values[idx];
    });
    result.push(obj);
  }
  return result;
}

function exportToCsv(dataArray, filename) {
  if (!dataArray || dataArray.length === 0) {
    showToast('Không có dữ liệu để xuất!', 'error');
    return;
  }
  const headers = Object.keys(dataArray[0]);
  const csvRows = [headers.join(',')];

  dataArray.forEach(row => {
    const values = headers.map(h => row[h] !== undefined ? row[h] : '');
    csvRows.push(values.join(','));
  });

  const blob = new Blob([csvRows.join('\n')], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
  showToast(`Đã tải xuống ${filename}`, 'info');
}

function exportResultsToCsv() {
  if (!state.solution || !state.solution.buses) {
    showToast('Chưa có kết quả để xuất!', 'error');
    return;
  }
  exportToCsv(state.solution.buses, 'power_flow_bus_results.csv');
  setTimeout(() => {
    exportToCsv(state.solution.branches, 'power_flow_branch_results.csv');
  }, 200);
}


// =============================================================================
// 9. HELPER FUNCTIONS & TOAST SYSTEM
// =============================================================================

function formatNum(num) {
  if (num === undefined || num === null || isNaN(num)) return '0';
  return parseFloat(num.toFixed(4)).toString();
}

function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  
  let icon = 'ℹ';
  if (type === 'success') icon = '✓';
  else if (type === 'error') icon = '⚠';

  toast.innerHTML = `<span class="font-bold">${icon}</span> <span>${message}</span>`;
  dom.toastContainer.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}
