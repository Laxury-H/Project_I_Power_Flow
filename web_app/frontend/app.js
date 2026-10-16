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
  demandScale: 100.0,
  trippedLines: [],
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
  demandScaleInput: document.getElementById('demandScaleInput'),
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

  // Split View Diagram
  gridSvg: document.getElementById('gridSvg'),
  layerLines: document.getElementById('layerLines'),
  layerFlowMarkers: document.getElementById('layerFlowMarkers'),
  layerBuses: document.getElementById('layerBuses'),
  btnAutoLayout: document.getElementById('btnAutoLayout'),
  btnZoomIn: document.getElementById('btnZoomIn'),
  btnZoomOut: document.getElementById('btnZoomOut'),
  btnResetView: document.getElementById('btnResetView'),

  // Full Screen View Diagram
  fullGridSvg: document.getElementById('fullGridSvg'),
  fullLayerLines: document.getElementById('fullLayerLines'),
  fullLayerFlowMarkers: document.getElementById('fullLayerFlowMarkers'),
  fullLayerBuses: document.getElementById('fullLayerBuses'),
  btnAutoLayoutFull: document.getElementById('btnAutoLayoutFull'),
  btnZoomInFull: document.getElementById('btnZoomInFull'),
  btnZoomOutFull: document.getElementById('btnZoomOutFull'),
  btnResetViewFull: document.getElementById('btnResetViewFull'),
  btnExportSvg: document.getElementById('btnExportSvg'),

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

  // Tab 5: Contingency & Security Audit
  btnAuditSecurity: document.getElementById('btnAuditSecurity'),
  auditVoltStatus: document.getElementById('auditVoltStatus'),
  auditVmin: document.getElementById('auditVmin'),
  auditAngleMax: document.getElementById('auditAngleMax'),
  auditPbalance: document.getElementById('auditPbalance'),
  auditViolationsSection: document.getElementById('auditViolationsSection'),
  auditViolationsTableBody: document.getElementById('auditViolationsTableBody'),

  tripLineSelect: document.getElementById('tripLineSelect'),
  btnTripLine: document.getElementById('btnTripLine'),
  restoreLineSelect: document.getElementById('restoreLineSelect'),
  btnRestoreLine: document.getElementById('btnRestoreLine'),

  btnRunN1: document.getElementById('btnRunN1'),
  n1TableBody: document.getElementById('n1TableBody'),

  btnRunPv: document.getElementById('btnRunPv'),
  pvTableBody: document.getElementById('pvTableBody'),
  pvChartWrapper: document.getElementById('pvChartWrapper'),

  // Tab 6: PyPower Verification
  btnRunPyPower: document.getElementById('btnRunPyPower'),
  pyPowerStatusBadge: document.getElementById('pyPowerStatusBadge'),
  pyPowerMaxVerr: document.getElementById('pyPowerMaxVerr'),
  pyPowerMaxAerr: document.getElementById('pyPowerMaxAerr'),
  pyPowerLossErr: document.getElementById('pyPowerLossErr'),
  pyPowerTableBody: document.getElementById('pyPowerTableBody'),

  interactiveTooltip: document.getElementById('interactiveTooltip'),
  toastContainer: document.getElementById('toastContainer')
};

// =============================================================================
// 1. INITIALIZATION & EVENT LISTENERS
// =============================================================================

document.addEventListener('DOMContentLoaded', async () => {
  setupNavigationTabs();
  setupGlobalControls();
  setupScenarioControls();
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
      const targetPane = document.getElementById(tabId);
      if (targetPane) targetPane.classList.add('active');
      state.activeTab = tabId;

      if (tabId === 'tab-ybus') {
        fetchAndRenderYbus();
      } else if (tabId === 'tab-diagram') {
        renderDiagram();
      } else if (tabId === 'tab-contingency') {
        updateBreakerSelects();
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

  if (dom.demandScaleInput) {
    dom.demandScaleInput.addEventListener('change', (e) => {
      const val = parseFloat(e.target.value);
      if (!isNaN(val) && val > 0) {
        state.demandScale = val;
        showToast(`Đã điều chỉnh quy mô phụ tải lên ${val}%`, 'info');
      }
    });
  }

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
    state.trippedLines = [];
    state.demandScale = 100.0;
    if (dom.demandScaleInput) dom.demandScaleInput.value = 100;
    state.baseMva = data.base_mva || 100.0;
    dom.baseMvaInput.value = state.baseMva;
    dom.presetSelect.value = presetId;
    state.solution = null;

    calculateNodePositions();
    renderTables();
    renderDiagram();
    triggerValidation();
    resetResultsView();
    updateBreakerSelects();

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
// 5. UPGRADED INTERACTIVE SVG DIAGRAM ENGINE (SCADA / CAD SINGLE-LINE DIAGRAM)
// =============================================================================

const diagramViews = {
  split: {
    svg: null,
    layers: { lines: null, flow: null, buses: null },
    vb: { x: 0, y: 0, w: 800, h: 600 },
    origVb: { x: 0, y: 0, w: 800, h: 600 },
    isPanning: false,
    panStart: { x: 0, y: 0 }
  },
  full: {
    svg: null,
    layers: { lines: null, flow: null, buses: null },
    vb: { x: 0, y: 0, w: 1000, h: 650 },
    origVb: { x: 0, y: 0, w: 1000, h: 650 },
    isPanning: false,
    panStart: { x: 0, y: 0 }
  }
};

let activeDraggedBusId = null;
let activeDragOffset = { x: 0, y: 0 };

function setupDiagramInteractions() {
  diagramViews.split.svg = dom.gridSvg;
  diagramViews.split.layers = {
    lines: dom.layerLines,
    flow: dom.layerFlowMarkers,
    buses: dom.layerBuses
  };

  diagramViews.full.svg = dom.fullGridSvg;
  diagramViews.full.layers = {
    lines: dom.fullLayerLines,
    flow: dom.fullLayerFlowMarkers,
    buses: dom.fullLayerBuses
  };

  // Wire controls for both toolbars
  setupSvgViewControls('split', dom.btnZoomIn, dom.btnZoomOut, dom.btnResetView, dom.btnAutoLayout);
  setupSvgViewControls('full', dom.btnZoomInFull, dom.btnZoomOutFull, dom.btnResetViewFull, dom.btnAutoLayoutFull);

  // SVG Export
  if (dom.btnExportSvg) {
    dom.btnExportSvg.addEventListener('click', exportSvgDiagram);
  }

  // Attach mouse dragging and wheel listeners for both SVGs
  attachSvgMouseEvents('split');
  attachSvgMouseEvents('full');

  // Window global mouse up
  window.addEventListener('mouseup', () => {
    activeDraggedBusId = null;
    diagramViews.split.isPanning = false;
    diagramViews.full.isPanning = false;
  });
}

function setupSvgViewControls(viewKey, btnIn, btnOut, btnReset, btnAuto) {
  const v = diagramViews[viewKey];

  if (btnIn) {
    btnIn.addEventListener('click', () => {
      zoomView(viewKey, 0.8);
    });
  }
  if (btnOut) {
    btnOut.addEventListener('click', () => {
      zoomView(viewKey, 1.25);
    });
  }
  if (btnReset) {
    btnReset.addEventListener('click', () => {
      resetView(viewKey);
    });
  }
  if (btnAuto) {
    btnAuto.addEventListener('click', () => {
      state.nodePositions = {};
      calculateNodePositions();
      renderDiagram();
      showToast('Đã tính toán và bố trí lại vị trí các trạm!', 'info');
    });
  }
}

function zoomView(viewKey, scaleFactor) {
  const v = diagramViews[viewKey];
  if (!v.svg) return;

  const curW = v.vb.w;
  const curH = v.vb.h;
  const newW = Math.max(300, Math.min(2500, curW * scaleFactor));
  const newH = Math.max(225, Math.min(1875, curH * scaleFactor));

  v.vb.x += (curW - newW) / 2;
  v.vb.y += (curH - newH) / 2;
  v.vb.w = newW;
  v.vb.h = newH;

  applyViewBox(viewKey);
}

function resetView(viewKey) {
  const v = diagramViews[viewKey];
  if (!v.svg) return;
  v.vb = { ...v.origVb };
  applyViewBox(viewKey);
}

function applyViewBox(viewKey) {
  const v = diagramViews[viewKey];
  if (v.svg) {
    v.svg.setAttribute('viewBox', `${v.vb.x} ${v.vb.y} ${v.vb.w} ${v.vb.h}`);
  }
}

function attachSvgMouseEvents(viewKey) {
  const v = diagramViews[viewKey];
  if (!v.svg) return;

  // Mouse wheel zoom
  v.svg.addEventListener('wheel', (e) => {
    e.preventDefault();
    const factor = e.deltaY > 0 ? 1.15 : 0.85;
    zoomView(viewKey, factor);
  }, { passive: false });

  // Mouse down: detect bus drag vs background pan
  v.svg.addEventListener('mousedown', (e) => {
    const busGroup = e.target.closest('.svg-bus-group');
    if (busGroup) {
      activeDraggedBusId = parseInt(busGroup.getAttribute('data-bus-id'));
      const pt = getSvgCursorPoint(v.svg, e);
      activeDragOffset.x = pt.x - state.nodePositions[activeDraggedBusId].x;
      activeDragOffset.y = pt.y - state.nodePositions[activeDraggedBusId].y;
    } else {
      v.isPanning = true;
      v.panStart = { x: e.clientX, y: e.clientY };
    }
  });

  v.svg.addEventListener('mousemove', (e) => {
    // 1. Drag Bus Node
    if (activeDraggedBusId !== null) {
      const pt = getSvgCursorPoint(v.svg, e);
      state.nodePositions[activeDraggedBusId].x = Math.round(pt.x - activeDragOffset.x);
      state.nodePositions[activeDraggedBusId].y = Math.round(pt.y - activeDragOffset.y);
      renderDiagram();
    }
    // 2. Pan Background
    else if (v.isPanning) {
      const dx = (e.clientX - v.panStart.x) * (v.vb.w / v.svg.clientWidth);
      const dy = (e.clientY - v.panStart.y) * (v.vb.h / v.svg.clientHeight);
      v.vb.x -= dx;
      v.vb.y -= dy;
      v.panStart = { x: e.clientX, y: e.clientY };
      applyViewBox(viewKey);
    }
  });
}

function getSvgCursorPoint(svgElem, e) {
  const pt = svgElem.createSVGPoint();
  pt.x = e.clientX;
  pt.y = e.clientY;
  return pt.matrixTransform(svgElem.getScreenCTM().inverse());
}

function calculateNodePositions() {
  const n = state.buses.length;
  if (n === 0) return;

  // Preset customized coordinates for iconic benchmarks
  if (state.presetId === '3bus' && n === 3) {
    state.nodePositions = {
      1: { x: 240, y: 220 }, // Slack (top-left)
      2: { x: 560, y: 220 }, // PV (top-right)
      3: { x: 400, y: 450 }  // PQ (bottom-center)
    };
    return;
  }

  if (state.presetId === '5bus' && n === 5) {
    state.nodePositions = {
      1: { x: 180, y: 220 }, // Slack
      2: { x: 620, y: 220 }, // PV
      3: { x: 260, y: 440 }, // PQ 3
      4: { x: 540, y: 440 }, // PQ 4
      5: { x: 400, y: 530 }  // PQ 5
    };
    return;
  }

  // Symmetric circular auto-layout for arbitrary N
  const cx = 400;
  const cy = 300;
  const radius = Math.min(240, 90 + n * 24);

  state.buses.forEach((b, i) => {
    if (!state.nodePositions[b.bus]) {
      const angle = (2 * Math.PI * i) / n - Math.PI / 2;
      state.nodePositions[b.bus] = {
        x: Math.round(cx + radius * Math.cos(angle)),
        y: Math.round(cy + radius * Math.sin(angle))
      };
    }
  });
}

function renderDiagram() {
  renderSvgInstance('split');
  renderSvgInstance('full');
}

function renderSvgInstance(viewKey) {
  const v = diagramViews[viewKey];
  if (!v.svg || !v.layers.lines) return;

  v.layers.lines.innerHTML = '';
  v.layers.flow.innerHTML = '';
  v.layers.buses.innerHTML = '';

  const isSolved = state.solution && state.solution.converged && state.solution.branches;
  const busSolMap = {};
  if (state.solution && state.solution.buses) {
    state.solution.buses.forEach(b => { busSolMap[b.bus] = b; });
  }

  // 1. RENDER TRANSMISSION LINES & FLOW BADGES
  state.lines.forEach((line, idx) => {
    const posA = state.nodePositions[line.from_bus];
    const posB = state.nodePositions[line.to_bus];
    if (!posA || !posB) return;

    const gLine = document.createElementNS('http://www.w3.org/2000/svg', 'g');

    // Base Transmission Line
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    path.setAttribute('x1', posA.x);
    path.setAttribute('y1', posA.y);
    path.setAttribute('x2', posB.x);
    path.setAttribute('y2', posB.y);
    path.setAttribute('class', 'svg-line');
    path.setAttribute('data-line-idx', idx);

    let branchSol = null;
    if (isSolved) {
      branchSol = state.solution.branches.find(b => b.from_bus === line.from_bus && b.to_bus === line.to_bus);
    }

    if (branchSol) {
      path.classList.add('svg-line-flow');
      
      // Determine actual flow direction
      const pFrom = branchSol.p_from_MW;
      const isReverse = pFrom < 0;
      const actualFrom = isReverse ? line.to_bus : line.from_bus;
      const actualTo = isReverse ? line.from_bus : line.to_bus;
      const pMagnitude = Math.abs(isReverse ? branchSol.p_to_MW : pFrom);

      // Midpoint for Flow Badge Pill
      const midX = (posA.x + posB.x) / 2;
      const midY = (posA.y + posB.y) / 2;

      // Group for Flow Badge
      const gBadge = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      gBadge.setAttribute('transform', `translate(${midX}, ${midY})`);

      const pillRect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      const pillWidth = 120;
      const pillHeight = 22;
      pillRect.setAttribute('x', -pillWidth / 2);
      pillRect.setAttribute('y', -pillHeight / 2);
      pillRect.setAttribute('width', pillWidth);
      pillRect.setAttribute('height', pillHeight);
      pillRect.setAttribute('class', 'svg-flow-pill');

      const pillText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      pillText.setAttribute('class', 'svg-flow-text');
      pillText.textContent = `${actualFrom} ➜ ${actualTo}: ${pMagnitude.toFixed(1)} MW`;

      gBadge.appendChild(pillRect);
      gBadge.appendChild(pillText);

      // Tooltip on flow badge
      gBadge.addEventListener('mouseenter', (e) => {
        let content = `<div class="tooltip-title">Đường dây ${line.from_bus} ➜ ${line.to_bus}</div>`;
        content += `<div class="tooltip-row"><span class="tooltip-label">P đầu gửi:</span> <span>${branchSol.p_from_MW.toFixed(2)} MW</span></div>`;
        content += `<div class="tooltip-row"><span class="tooltip-label">Q đầu gửi:</span> <span>${branchSol.q_from_Mvar.toFixed(2)} Mvar</span></div>`;
        content += `<div class="tooltip-row"><span class="tooltip-label">P đầu nhận:</span> <span>${branchSol.p_to_MW.toFixed(2)} MW</span></div>`;
        content += `<div class="tooltip-row"><span class="tooltip-label">Q đầu nhận:</span> <span>${branchSol.q_to_Mvar.toFixed(2)} Mvar</span></div>`;
        content += `<div class="tooltip-row"><span class="tooltip-label">Tổn thất ΔP:</span> <span class="text-danger font-bold">${branchSol.p_loss_MW.toFixed(4)} MW</span></div>`;
        content += `<div class="tooltip-row"><span class="tooltip-label">Tổn thất ΔQ:</span> <span>${branchSol.q_loss_Mvar.toFixed(4)} Mvar</span></div>`;
        content += `<div class="tooltip-row"><span class="tooltip-label">Dòng điện:</span> <span>${branchSol.current_pu.toFixed(4)} pu</span></div>`;
        showTooltip(e, content);
      });
      gBadge.addEventListener('mouseleave', hideTooltip);

      v.layers.flow.appendChild(gBadge);
    }

    // Line tooltip
    path.addEventListener('mouseenter', (e) => {
      let content = `<div class="tooltip-title">Đường dây ${line.from_bus} ➜ ${line.to_bus}</div>`;
      content += `<div class="tooltip-row"><span class="tooltip-label">Điện trở R:</span> <span>${line.r_pu} pu</span></div>`;
      content += `<div class="tooltip-row"><span class="tooltip-label">Điện kháng X:</span> <span>${line.x_pu} pu</span></div>`;
      if (branchSol) {
        content += `<div class="tooltip-row"><span class="tooltip-label">Tổn thất ΔP:</span> <span class="text-danger font-bold">${branchSol.p_loss_MW.toFixed(4)} MW</span></div>`;
        content += `<div class="tooltip-row"><span class="tooltip-label">Dòng |I|:</span> <span>${branchSol.current_pu.toFixed(4)} pu</span></div>`;
      }
      showTooltip(e, content);
    });
    path.addEventListener('mouseleave', hideTooltip);

    gLine.appendChild(path);
    v.layers.lines.appendChild(gLine);
  });

  // 2. RENDER BUSES WITH ELECTRICAL GENERATOR & LOAD SYMBOLS
  state.buses.forEach(b => {
    const pos = state.nodePositions[b.bus];
    if (!pos) return;

    const gBus = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    gBus.setAttribute('class', 'svg-bus-group');
    gBus.setAttribute('data-bus-id', b.bus);
    gBus.setAttribute('transform', `translate(${pos.x}, ${pos.y})`);

    const busSol = busSolMap[b.bus];

    // Determine electrical attachments
    const hasGen = (b.type === 'Slack' || b.type === 'PV');
    const pdVal = b.pd_pu * state.baseMva;
    const qdVal = b.qd_pu * state.baseMva;
    const hasLoad = (b.type === 'PQ' || pdVal > 0.1 || qdVal > 0.1);

    // --- A. GENERATOR ATTACHMENT (FOR SLACK & PV) ---
    if (hasGen) {
      const gGen = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      
      // Generator connecting stub line
      const stub = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      stub.setAttribute('x1', 0);
      stub.setAttribute('y1', -24);
      stub.setAttribute('x2', 0);
      stub.setAttribute('y2', -44);
      stub.setAttribute('stroke', b.type === 'Slack' ? '#EC4899' : '#F59E0B');
      stub.setAttribute('stroke-width', 2);

      // Generator circle
      const genCircle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
      genCircle.setAttribute('cx', 0);
      genCircle.setAttribute('cy', -58);
      genCircle.setAttribute('r', 14);
      genCircle.setAttribute('class', 'svg-gen-circle');
      genCircle.setAttribute('stroke', b.type === 'Slack' ? '#EC4899' : '#F59E0B');
      genCircle.setAttribute('fill', b.type === 'Slack' ? 'rgba(236, 72, 153, 0.25)' : 'rgba(245, 158, 11, 0.25)');

      // Sine wave symbol (~) inside generator
      const genWave = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      genWave.setAttribute('d', 'M -8 -58 Q -4 -63 0 -58 Q 4 -53 8 -58');
      genWave.setAttribute('class', 'svg-gen-wave');
      genWave.setAttribute('stroke', b.type === 'Slack' ? '#EC4899' : '#F59E0B');

      // Generator power label
      const genText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      genText.setAttribute('x', 0);
      genText.setAttribute('y', -78);
      genText.setAttribute('class', 'svg-bus-label');
      genText.setAttribute('fill', b.type === 'Slack' ? '#F472B6' : '#FBBF24');
      
      if (busSol) {
        genText.textContent = `P: ${busSol.pg_MW.toFixed(1)} MW`;
      } else {
        const pgVal = (b.pg_pu * state.baseMva).toFixed(1);
        genText.textContent = b.type === 'Slack' ? 'G (Slack)' : `G (${pgVal} MW)`;
      }

      gGen.appendChild(stub);
      gGen.appendChild(genCircle);
      gGen.appendChild(genWave);
      gGen.appendChild(genText);
      gBus.appendChild(gGen);
    }

    // --- B. LOAD ATTACHMENT (FOR PQ OR BUSES WITH DEMAND > 0) ---
    if (hasLoad) {
      const gLoad = document.createElementNS('http://www.w3.org/2000/svg', 'g');

      // Stub line downward
      const loadLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      loadLine.setAttribute('x1', 0);
      loadLine.setAttribute('y1', 24);
      loadLine.setAttribute('x2', 0);
      loadLine.setAttribute('y2', 46);
      loadLine.setAttribute('stroke', '#06B6D4');
      loadLine.setAttribute('stroke-width', 2);

      // Downward arrow
      const arrowHead = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
      arrowHead.setAttribute('points', '-6,46 6,46 0,55');
      arrowHead.setAttribute('fill', '#06B6D4');

      // Load Value Badge
      const badgeRect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      badgeRect.setAttribute('x', -44);
      badgeRect.setAttribute('y', 58);
      badgeRect.setAttribute('width', 88);
      badgeRect.setAttribute('height', 18);
      badgeRect.setAttribute('class', 'svg-load-badge');

      const loadText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
      loadText.setAttribute('x', 0);
      loadText.setAttribute('y', 67);
      loadText.setAttribute('class', 'svg-load-text');
      loadText.textContent = `${pdVal.toFixed(0)}MW, ${qdVal.toFixed(0)}Mvar`;

      gLoad.appendChild(loadLine);
      gLoad.appendChild(arrowHead);
      gLoad.appendChild(badgeRect);
      gLoad.appendChild(loadText);
      gBus.appendChild(gLoad);
    }

    // --- C. MAIN SUBSTATION BUS CIRCLE ---
    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('r', 24);
    circle.setAttribute('class', 'svg-bus-circle');

    let strokeCol = '#06B6D4';
    let fillCol = 'rgba(6, 182, 212, 0.25)';
    if (b.type === 'Slack') {
      strokeCol = '#EC4899';
      fillCol = 'rgba(236, 72, 153, 0.35)';
    } else if (b.type === 'PV') {
      strokeCol = '#F59E0B';
      fillCol = 'rgba(245, 158, 11, 0.35)';
    }

    circle.setAttribute('stroke', strokeCol);
    circle.setAttribute('fill', fillCol);

    // Bus Number in Center
    const textId = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    textId.setAttribute('class', 'svg-bus-text');
    textId.textContent = b.bus;

    // Adaptive positioning to avoid collision between Generator (top) and Load (bottom)
    let typeY = -30;
    let voltX = 0;
    let voltY = 34;

    if (hasGen && hasLoad) {
      typeY = -92;
      voltX = 56;
      voltY = 0;
    } else if (hasGen) {
      typeY = -92;
      voltX = 0;
      voltY = 34;
    } else if (hasLoad) {
      typeY = -48;
      voltX = 0;
      voltY = -28;
    } else {
      typeY = -30;
      voltX = 0;
      voltY = 34;
    }

    // Bus Header Type Badge
    const typeLabel = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    typeLabel.setAttribute('x', 0);
    typeLabel.setAttribute('y', typeY);
    typeLabel.setAttribute('class', 'svg-bus-label');
    typeLabel.setAttribute('fill', strokeCol);
    typeLabel.textContent = `${b.type} ${b.bus}`;

    // Solved Voltage & Angle Pill
    const gVoltPill = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    gVoltPill.setAttribute('transform', `translate(${voltX}, ${voltY})`);

    const voltRect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    voltRect.setAttribute('x', -48);
    voltRect.setAttribute('y', -9);
    voltRect.setAttribute('width', 96);
    voltRect.setAttribute('height', 18);
    voltRect.setAttribute('class', 'svg-badge-rect');

    const voltText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    voltText.setAttribute('class', 'svg-bus-label');
    voltText.setAttribute('y', 0);
    voltText.setAttribute('fill', '#E2E8F0');
    
    if (busSol) {
      voltText.textContent = `${busSol.vm_pu.toFixed(3)}∠${busSol.va_deg.toFixed(1)}°`;
    } else {
      voltText.textContent = `${b.vm_pu}∠${b.va_deg}°`;
    }

    gVoltPill.appendChild(voltRect);
    gVoltPill.appendChild(voltText);

    gBus.appendChild(circle);
    gBus.appendChild(textId);
    gBus.appendChild(typeLabel);
    gBus.appendChild(gVoltPill);

    // Hover Tooltip with comprehensive engineering telemetry
    gBus.addEventListener('mouseenter', (e) => {
      let content = `<div class="tooltip-title">Thanh cái Bus ${b.bus} [${b.type}]</div>`;
      if (busSol) {
        content += `<div class="tooltip-row"><span class="tooltip-label">Điện áp |V|:</span> <span class="font-bold text-primary">${busSol.vm_pu} pu</span></div>`;
        content += `<div class="tooltip-row"><span class="tooltip-label">Góc pha δ:</span> <span>${busSol.va_deg}° (${busSol.va_rad} rad)</span></div>`;
        content += `<div class="tooltip-row"><span class="tooltip-label">P phát:</span> <span>${busSol.pg_MW.toFixed(2)} MW</span></div>`;
        content += `<div class="tooltip-row"><span class="tooltip-label">Q phát:</span> <span>${busSol.qg_Mvar.toFixed(2)} Mvar</span></div>`;
        content += `<div class="tooltip-row"><span class="tooltip-label">P tải:</span> <span>${busSol.pd_MW.toFixed(2)} MW</span></div>`;
        content += `<div class="tooltip-row"><span class="tooltip-label">Q tải:</span> <span>${busSol.qd_Mvar.toFixed(2)} Mvar</span></div>`;
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

    v.layers.buses.appendChild(gBus);
  });
}

function exportSvgDiagram() {
  const svg = dom.fullGridSvg || dom.gridSvg;
  if (!svg) return;

  const serializer = new XMLSerializer();
  let source = serializer.serializeToString(svg);

  // Add XML declaration & namespaces if missing
  if (!source.match(/^<svg[^>]+xmlns="http\:\/\/www\.w3\.org\/2000\/svg"/)) {
    source = source.replace(/^<svg/, '<svg xmlns="http://www.w3.org/2000/svg"');
  }

  const blob = new Blob([source], { type: 'image/svg+xml;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `power_flow_diagram_${state.presetId}.svg`;
  a.click();
  URL.revokeObjectURL(url);
  showToast('Đã tải xuống sơ đồ lưới điện định dạng SVG!', 'success');
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
        demand_scale: state.demandScale,
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


// =============================================================================
// 10. ADVANCED SCENARIO ANALYSIS, N-1 CONTINGENCY & PYPOWER BENCHMARKING
// =============================================================================

function setupScenarioControls() {
  if (dom.btnAuditSecurity) {
    dom.btnAuditSecurity.addEventListener('click', runSecurityAudit);
  }
  if (dom.btnTripLine) {
    dom.btnTripLine.addEventListener('click', tripSelectedLine);
  }
  if (dom.btnRestoreLine) {
    dom.btnRestoreLine.addEventListener('click', restoreSelectedLine);
  }
  if (dom.btnRunN1) {
    dom.btnRunN1.addEventListener('click', runN1Contingency);
  }
  if (dom.btnRunPv) {
    dom.btnRunPv.addEventListener('click', runPvLoadStress);
  }
  if (dom.btnRunPyPower) {
    dom.btnRunPyPower.addEventListener('click', runPyPowerVerification);
  }
}

function updateBreakerSelects() {
  if (!dom.tripLineSelect || !dom.restoreLineSelect) return;

  // Active in-service lines
  dom.tripLineSelect.innerHTML = '';
  if (state.lines.length === 0) {
    dom.tripLineSelect.innerHTML = '<option value="">(Không có đường dây nào)</option>';
    if (dom.btnTripLine) dom.btnTripLine.disabled = true;
  } else {
    state.lines.forEach((l, idx) => {
      const opt = document.createElement('option');
      opt.value = idx;
      opt.textContent = `Đường dây ${l.from_bus} ➔ ${l.to_bus} (R=${l.r_pu}, X=${l.x_pu})`;
      dom.tripLineSelect.appendChild(opt);
    });
    if (dom.btnTripLine) dom.btnTripLine.disabled = state.lines.length <= 1;
  }

  // Tripped lines
  dom.restoreLineSelect.innerHTML = '';
  if (state.trippedLines.length === 0) {
    dom.restoreLineSelect.innerHTML = '<option value="">(Không có đường dây nào đang cắt)</option>';
    if (dom.btnRestoreLine) dom.btnRestoreLine.disabled = true;
  } else {
    state.trippedLines.forEach((l, idx) => {
      const opt = document.createElement('option');
      opt.value = idx;
      opt.textContent = `Đường dây ${l.from_bus} ➔ ${l.to_bus} (ĐÃ CẮT SỰ CỐ)`;
      dom.restoreLineSelect.appendChild(opt);
    });
    if (dom.btnRestoreLine) dom.btnRestoreLine.disabled = false;
  }
}

function tripSelectedLine() {
  const selIdx = parseInt(dom.tripLineSelect.value);
  if (isNaN(selIdx) || selIdx < 0 || selIdx >= state.lines.length) {
    showToast('Vui lòng chọn đường dây cần cắt!', 'error');
    return;
  }
  const [tripped] = state.lines.splice(selIdx, 1);
  state.trippedLines.push(tripped);

  markCustomPreset();
  renderTables();
  renderDiagram();
  triggerValidation();
  updateBreakerSelects();
  showToast(`🔴 ĐÃ CẮT ĐƯỜNG DÂY ${tripped.from_bus} ➔ ${tripped.to_bus}!`, 'error');
}

function restoreSelectedLine() {
  const selIdx = parseInt(dom.restoreLineSelect.value);
  if (isNaN(selIdx) || selIdx < 0 || selIdx >= state.trippedLines.length) {
    showToast('Vui lòng chọn đường dây cần đóng lại!', 'error');
    return;
  }
  const [restored] = state.trippedLines.splice(selIdx, 1);
  state.lines.push(restored);

  markCustomPreset();
  renderTables();
  renderDiagram();
  triggerValidation();
  updateBreakerSelects();
  showToast(`🟢 ĐÃ ĐÓNG LẠI ĐƯỜNG DÂY ${restored.from_bus} ➔ ${restored.to_bus}!`, 'success');
}

async function runSecurityAudit() {
  if (!dom.btnAuditSecurity) return;
  dom.btnAuditSecurity.disabled = true;
  dom.btnAuditSecurity.textContent = '⏳ Đang kiểm định...';

  try {
    const res = await fetch('/api/security-audit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        buses: state.buses,
        lines: state.lines,
        base_mva: state.baseMva,
        demand_scale: state.demandScale
      })
    });
    if (!res.ok) throw new Error('Kiểm định an toàn thất bại');
    const data = await res.json();

    const isCompliant = data.is_fully_compliant;
    if (isCompliant) {
      dom.auditVoltStatus.className = 'kpi-value text-success';
      dom.auditVoltStatus.textContent = 'ĐẠT CHUẨN (N-0)';
    } else {
      dom.auditVoltStatus.className = 'kpi-value text-danger';
      dom.auditVoltStatus.textContent = `VI PHẠM (${data.violations_count} vi phạm)`;
    }

    dom.auditVmin.textContent = data.v_min_observed !== undefined ? `${data.v_min_observed.toFixed(4)} pu` : '—';
    dom.auditAngleMax.textContent = data.max_angle_diff_deg !== undefined ? `${data.max_angle_diff_deg.toFixed(2)}°` : '—';
    const pBal = data.p_balance_err_MW;
    dom.auditPbalance.textContent = (pBal !== undefined && pBal < 1e-10) ? '< 10⁻¹² MW' : (pBal !== undefined ? `${pBal.toExponential(3)} MW` : '—');

    // Combine violations
    const violations = [];
    if (data.critical_low_voltage_buses) {
      data.critical_low_voltage_buses.forEach(b => violations.push({
        bus: b.bus, type: b.type, vm_pu: b.vm_pu, desc: `Điện áp thấp < ${b.limit_pu || 0.95} pu`
      }));
    }
    if (data.critical_high_voltage_buses) {
      data.critical_high_voltage_buses.forEach(b => violations.push({
        bus: b.bus, type: b.type, vm_pu: b.vm_pu, desc: `Điện áp cao > ${b.limit_pu || 1.05} pu`
      }));
    }
    if (data.angle_violations) {
      data.angle_violations.forEach(a => violations.push({
        bus: `${a.from_bus} ➔ ${a.to_bus}`, type: 'Đường dây', vm_pu: a.angle_diff_deg, desc: `Lệch pha ${a.angle_diff_deg.toFixed(1)}° > 30°`
      }));
    }

    if (violations.length > 0 && dom.auditViolationsSection) {
      dom.auditViolationsSection.style.display = 'block';
      dom.auditViolationsTableBody.innerHTML = violations.map(v => `
        <tr>
          <td><strong>Bus ${v.bus}</strong></td>
          <td><span class="bus-badge badge-${v.type ? v.type.toLowerCase() : 'pv'}">${v.type}</span></td>
          <td class="font-mono font-bold text-danger">${typeof v.vm_pu === 'number' ? v.vm_pu.toFixed(4) : v.vm_pu}</td>
          <td><span class="bus-badge badge-status-err">${v.desc}</span></td>
        </tr>
      `).join('');
    } else if (dom.auditViolationsSection) {
      dom.auditViolationsSection.style.display = 'none';
    }

    showToast(isCompliant ? 'Đạt toàn bộ tiêu chuẩn vận hành an toàn Grid Code N-0!' : `Phát hiện ${data.violations_count} vi phạm điện áp/góc pha!`, isCompliant ? 'success' : 'warning');
  } catch (err) {
    showToast(`Lỗi kiểm tra quy chuẩn: ${err.message}`, 'error');
  } finally {
    dom.btnAuditSecurity.disabled = false;
    dom.btnAuditSecurity.textContent = '🛡️ Quét tuân thủ N-0';
  }
}

async function runN1Contingency() {
  if (!dom.btnRunN1) return;
  dom.btnRunN1.disabled = true;
  dom.btnRunN1.textContent = '⏳ Đang quét N-1...';

  try {
    const res = await fetch('/api/contingency-n1', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        buses: state.buses,
        lines: state.lines,
        base_mva: state.baseMva,
        demand_scale: state.demandScale
      })
    });
    if (!res.ok) throw new Error('Quét sự cố N-1 thất bại');
    const data = await res.json();
    const records = Array.isArray(data) ? data : (data.contingencies || []);

    if (records.length === 0) {
      dom.n1TableBody.innerHTML = '<tr><td colspan="9" class="text-center text-muted">Không có đường dây nào để quét!</td></tr>';
      return;
    }

    dom.n1TableBody.innerHTML = records.map((c, idx) => {
      let severityClass = 'badge-status-ok';
      if (c.risk_level && c.risk_level.includes('Cảnh báo')) severityClass = 'badge-status-warn';
      else if (c.risk_level && (c.risk_level.includes('Nghiêm trọng') || c.risk_level.includes('Không hội tụ') || c.risk_level.includes('Phân đảo') || c.risk_level.includes('Cực kỳ'))) severityClass = 'badge-status-err';

      const vMinDisplay = c.v_min_pu !== null && c.v_min_pu !== undefined ? `${c.v_min_pu.toFixed(4)} pu` : '—';
      const lossDisplay = c.p_loss_MW !== null && c.p_loss_MW !== undefined ? `${c.p_loss_MW.toFixed(3)} MW` : '—';
      const incDisplay = c.loss_delta_MW !== null && c.loss_delta_MW !== undefined ? `${c.loss_delta_MW >= 0 ? '+' : ''}${c.loss_delta_MW.toFixed(3)} MW` : '—';

      return `
        <tr>
          <td><strong>#${idx + 1}</strong></td>
          <td><span class="font-bold">Đường dây ${c.outage}</span></td>
          <td>${c.converged ? '<span class="bus-badge badge-status-ok">Hội tụ</span>' : '<span class="bus-badge badge-status-err">Mất hội tụ</span>'}</td>
          <td>${c.iterations ? c.iterations + ' vòng' : '—'}</td>
          <td class="font-mono font-bold">${vMinDisplay}</td>
          <td>${c.worst_bus || '—'}</td>
          <td class="font-mono">${lossDisplay}</td>
          <td class="font-mono">${incDisplay}</td>
          <td><span class="bus-badge ${severityClass}">${c.risk_level || c.status}</span></td>
        </tr>
      `;
    }).join('');

    const warnCount = records.filter(r => r.risk_level && r.risk_level.includes('Cảnh báo')).length;
    const critCount = records.filter(r => r.risk_level && (r.risk_level.includes('Nghiêm trọng') || r.risk_level.includes('Không hội tụ') || r.risk_level.includes('Phân đảo'))).length;
    showToast(`Quét xong N-1: ${records.length} trường hợp sự cố (Cảnh báo: ${warnCount}, Nguy cấp: ${critCount})`, 'info');
  } catch (err) {
    showToast(`Lỗi quét N-1: ${err.message}`, 'error');
  } finally {
    dom.btnRunN1.disabled = false;
    dom.btnRunN1.textContent = '🚀 Quét toàn bộ sự cố N-1';
  }
}

async function runPvLoadStress() {
  if (!dom.btnRunPv) return;
  dom.btnRunPv.disabled = true;
  dom.btnRunPv.textContent = '⏳ Đang quét tải...';

  try {
    const res = await fetch('/api/load-stress', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        buses: state.buses,
        lines: state.lines,
        base_mva: state.baseMva
      })
    });
    if (!res.ok) throw new Error('Khảo sát P-V thất bại');
    const data = await res.json();
    const points = Array.isArray(data) ? data : (data.points || []);

    if (points.length === 0) {
      dom.pvTableBody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">Không có dữ liệu P-V!</td></tr>';
      return;
    }

    dom.pvTableBody.innerHTML = points.map(p => {
      const isOk = p.converged;
      const statusBadge = isOk ? '<span class="bus-badge badge-status-ok">Hội tụ</span>' : '<span class="bus-badge badge-status-err">Sụp đổ</span>';
      return `
        <tr>
          <td><strong>${p.scale_pct}%</strong></td>
          <td class="font-mono">${p.demand_MW !== null && p.demand_MW !== undefined ? p.demand_MW.toFixed(2) : '—'}</td>
          <td>${statusBadge}</td>
          <td class="font-mono font-bold ${(p.v_min_pu !== null && p.v_min_pu < 0.95) ? 'text-danger' : 'text-primary'}">${p.v_min_pu !== null && p.v_min_pu !== undefined ? p.v_min_pu.toFixed(4) : '—'}</td>
          <td>${p.worst_bus || '—'}</td>
          <td class="font-mono">${p.p_loss_MW !== null && p.p_loss_MW !== undefined ? p.p_loss_MW.toFixed(3) : '—'}</td>
        </tr>
      `;
    }).join('');

    renderPvCurve(points);
    const convergedPts = points.filter(p => p.converged);
    const maxScale = convergedPts.length > 0 ? Math.max(...convergedPts.map(p => p.scale_pct)) : 100;
    const margin = maxScale - 100;
    showToast(`Khảo sát P-V thành công! Dự phòng quá tải điện áp: +${margin}%`, 'info');
  } catch (err) {
    showToast(`Lỗi khảo sát P-V: ${err.message}`, 'error');
  } finally {
    dom.btnRunPv.disabled = false;
    dom.btnRunPv.textContent = '📈 Khảo sát đường cong P-V';
  }
}

function renderPvCurve(points) {
  if (!dom.pvChartWrapper) return;
  const validPts = points.filter(p => p.converged && p.demand_MW !== null && p.v_min_pu !== null);
  if (validPts.length < 2) {
    dom.pvChartWrapper.innerHTML = '<div class="empty-state"><div class="empty-icon">⚠️</div><div class="empty-text">Không đủ điểm hội tụ để dựng đường cong P-V</div></div>';
    return;
  }

  const w = 540;
  const h = 280;
  const padL = 55;
  const padR = 30;
  const padT = 30;
  const padB = 40;
  const chartW = w - padL - padR;
  const chartH = h - padT - padB;

  const pMin = Math.min(...validPts.map(p => p.demand_MW)) * 0.9;
  const pMax = Math.max(...validPts.map(p => p.demand_MW)) * 1.08;
  const vMin = Math.min(0.70, Math.min(...validPts.map(p => p.v_min_pu)) * 0.95);
  const vMax = Math.max(1.10, Math.max(...validPts.map(p => p.v_min_pu)) * 1.02);

  const getX = (val) => padL + ((val - pMin) / (pMax - pMin)) * chartW;
  const getY = (val) => padT + chartH * (1 - (val - vMin) / (vMax - vMin));

  let svg = `<svg viewBox="0 0 ${w} ${h}" class="pv-svg" style="width:100%; height:100%; overflow:visible;">`;

  // Grid Lines
  for (let v = Math.ceil(vMin * 10) / 10; v <= vMax; v += 0.1) {
    const y = getY(v);
    svg += `<line x1="${padL}" y1="${y}" x2="${w - padR}" y2="${y}" stroke="#1E293B" stroke-width="1" />`;
    svg += `<text x="${padL - 8}" y="${y + 4}" fill="#64748B" font-size="10" text-anchor="end" font-family="JetBrains Mono">${v.toFixed(2)}</text>`;
  }

  // Statutory Limit Line (0.95 pu)
  const y95 = getY(0.95);
  svg += `<line x1="${padL}" y1="${y95}" x2="${w - padR}" y2="${y95}" stroke="#F59E0B" stroke-width="1.5" stroke-dasharray="4,4" />`;
  svg += `<text x="${w - padR - 5}" y="${y95 - 6}" fill="#F59E0B" font-size="9" text-anchor="end" font-family="Inter">Ngưỡng 0.95 pu</text>`;

  // Axes
  svg += `<line x1="${padL}" y1="${padT}" x2="${padL}" y2="${h - padB}" stroke="#475569" stroke-width="1.5" />`;
  svg += `<line x1="${padL}" y1="${h - padB}" x2="${w - padR}" y2="${h - padB}" stroke="#475569" stroke-width="1.5" />`;

  // X-ticks
  const pStep = (pMax - pMin) / 4;
  for (let i = 0; i <= 4; i++) {
    const pVal = pMin + i * pStep;
    const x = getX(pVal);
    svg += `<line x1="${x}" y1="${h - padB}" x2="${x}" y2="${h - padB + 5}" stroke="#475569" stroke-width="1" />`;
    svg += `<text x="${x}" y="${h - padB + 18}" fill="#64748B" font-size="10" text-anchor="middle" font-family="JetBrains Mono">${pVal.toFixed(1)}</text>`;
  }

  // Axis Labels
  svg += `<text x="${padL + chartW / 2}" y="${h - 6}" fill="#94A3B8" font-size="11" text-anchor="middle" font-family="Inter" font-weight="600">Tổng công suất tải P_load (MW)</text>`;
  svg += `<text x="16" y="${padT + chartH / 2}" fill="#94A3B8" font-size="11" text-anchor="middle" font-family="Inter" font-weight="600" transform="rotate(-90 16 ${padT + chartH / 2})">Điện áp thấp nhất V_min (pu)</text>`;

  // P-V Trajectory Path
  let dPath = '';
  validPts.forEach((pt, i) => {
    const x = getX(pt.demand_MW);
    const y = getY(pt.v_min_pu);
    dPath += (i === 0 ? `M ${x} ${y}` : ` L ${x} ${y}`);
  });
  svg += `<path d="${dPath}" fill="none" stroke="#38BDF8" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />`;

  // Data Points
  validPts.forEach(pt => {
    const x = getX(pt.demand_MW);
    const y = getY(pt.v_min_pu);
    svg += `<circle cx="${x}" cy="${y}" r="4" fill="#0284C7" stroke="#38BDF8" stroke-width="1.5">
      <title>${pt.scale_pct}% Tải: ${pt.demand_MW.toFixed(1)} MW ➔ Vmin = ${pt.v_min_pu.toFixed(4)} pu (${pt.worst_bus})</title>
    </circle>`;
  });

  // Nose point annotation
  const criticalPt = validPts[validPts.length - 1];
  if (criticalPt && criticalPt.demand_MW) {
    const nx = getX(criticalPt.demand_MW);
    const ny = getY(criticalPt.v_min_pu);
    svg += `<circle cx="${nx}" cy="${ny}" r="7" fill="#EF4444" stroke="#FFFFFF" stroke-width="2" />`;
    svg += `<text x="${nx}" y="${ny - 12}" fill="#EF4444" font-size="10" text-anchor="middle" font-weight="bold" font-family="Inter">Điểm tới hạn (Nose Point)</text>`;
  }

  svg += `</svg>`;
  dom.pvChartWrapper.innerHTML = svg;
}

async function runPyPowerVerification() {
  if (!dom.btnRunPyPower) return;
  dom.btnRunPyPower.disabled = true;
  dom.btnRunPyPower.textContent = '⚡ Đang đối chuẩn...';

  try {
    const res = await fetch('/api/verify-pypower', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        buses: state.buses,
        lines: state.lines,
        base_mva: state.baseMva
      })
    });
    if (!res.ok) throw new Error('Đối chuẩn thất bại');
    const data = await res.json();

    const isPass = data.status === 'PASS';
    dom.pyPowerStatusBadge.className = isPass ? 'kpi-value text-success' : 'kpi-value text-danger';
    dom.pyPowerStatusBadge.textContent = isPass ? 'HOÀN HẢO (PASS)' : (data.status || 'FAIL');

    dom.pyPowerMaxVerr.textContent = data.max_voltage_error_pu !== null ? `${data.max_voltage_error_pu.toExponential(3)} pu` : '—';
    dom.pyPowerMaxAerr.textContent = data.max_angle_error_deg !== null ? `${data.max_angle_error_deg.toExponential(3)} °` : '—';
    dom.pyPowerLossErr.textContent = data.loss_error_MW !== null ? `${data.loss_error_MW.toExponential(3)} MW` : '—';

    if (data.comparison && data.comparison.length > 0) {
      dom.pyPowerTableBody.innerHTML = data.comparison.map(row => {
        const passPill = row.status === 'PASS' 
          ? '<span class="bus-badge badge-status-ok">PASS</span>'
          : '<span class="bus-badge badge-status-warn">WARN</span>';

        return `
          <tr>
            <td><strong>Bus ${row.bus}</strong></td>
            <td><span class="bus-badge badge-${row.type ? row.type.toLowerCase() : 'pv'}">${row.type}</span></td>
            <td class="font-mono">${row.v_project_pu.toFixed(5)}</td>
            <td class="font-mono">${row.v_pypower_pu.toFixed(5)}</td>
            <td class="font-mono font-bold text-success">${row.v_diff_pu}</td>
            <td class="font-mono">${row.va_project_deg.toFixed(3)}°</td>
            <td class="font-mono">${row.va_pypower_deg.toFixed(3)}°</td>
            <td class="font-mono font-bold text-success">${row.va_diff_deg}</td>
            <td>${passPill}</td>
          </tr>
        `;
      }).join('');
    }

    showToast(data.message || `Đối chuẩn hoàn tất: ${data.status}`, isPass ? 'success' : 'warning');
  } catch (err) {
    showToast(`Lỗi đối chuẩn PyPower: ${err.message}`, 'error');
  } finally {
    dom.btnRunPyPower.disabled = false;
    dom.btnRunPyPower.textContent = '⚡ Chạy đối chuẩn PyPower';
  }
}

