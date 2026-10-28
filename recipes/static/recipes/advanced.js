function AdvancedFilter() {
  const [selected, setSelected] = React.useState([]);
  const [filterText, setFilterText] = React.useState("");

  // Read initial ingredients from the hidden select or window
  const initialIngredients = React.useMemo(() => {
    const rawOptions = document.querySelectorAll("#raw-ingredient-source option");
    const list = [];
    rawOptions.forEach(opt => {
      const val = opt.value ? opt.value.trim() : "";
      if (val) list.push(val);
    });
    return list;
  }, []);

  const filteredIngredients = React.useMemo(() => {
    if (!filterText.trim()) return initialIngredients;
    const q = filterText.toLowerCase();
    return initialIngredients.filter(item => item.toLowerCase().includes(q));
  }, [filterText, initialIngredients]);

  const handleAdd = (val) => {
    if (val && !selected.includes(val)) {
      setSelected(prev => [...prev, val]);
    }
  };

  const handleRemove = (val) => {
    setSelected(prev => prev.filter(item => item !== val));
  };

  const handleClear = () => {
    setSelected([]);
  };

  return (
    <div>
      <div className="row g-4">
        {/* Available Ingredients */}
        <div className="col-md-7">
          <div className="d-flex justify-content-between align-items-center mb-2">
            <label className="form-label fw-bold mb-0 text-dark">
              <i className="bi bi-list-check text-primary me-1"></i> Available Ingredients ({filteredIngredients.length})
            </label>
            <span className="text-muted small">Double-click to select</span>
          </div>

          <div className="position-relative mb-2">
            <input
              type="text"
              className="form-control rounded-pill px-3 py-2 small"
              placeholder="Type to filter ingredients (e.g. chicken, cheese, garlic)..."
              value={filterText}
              onChange={(e) => setFilterText(e.target.value)}
              style={{ paddingRight: '2.5rem', fontSize: '0.9rem' }}
            />
            {filterText && (
              <button
                type="button"
                className="btn btn-sm btn-link position-absolute end-0 top-50 translate-middle-y text-muted text-decoration-none me-2"
                onClick={() => setFilterText("")}
              >
                <i className="bi bi-x-circle-fill"></i>
              </button>
            )}
          </div>

          <select
            className="form-select ingredient-select-box"
            size="14"
            onChange={(e) => handleAdd(e.target.value)}
            onDoubleClick={(e) => handleAdd(e.target.value)}
          >
            {filteredIngredients.map((item, idx) => (
              <option key={idx} value={item} className="py-1 px-2">
                {item}
              </option>
            ))}
          </select>
        </div>

        {/* Selected Ingredients */}
        <div className="col-md-5">
          <div className="d-flex justify-content-between align-items-center mb-2">
            <label className="form-label fw-bold mb-0 text-dark">
              <i className="bi bi-check-circle-fill text-success me-1"></i> Selected ({selected.length})
            </label>
            {selected.length > 0 && (
              <button
                type="button"
                className="btn btn-sm btn-link text-danger text-decoration-none p-0 small"
                onClick={handleClear}
              >
                Clear all
              </button>
            )}
          </div>

          <div
            className="p-3 bg-light rounded-4 border"
            style={{ minHeight: '340px', maxHeight: '420px', overflowY: 'auto' }}
          >
            {selected.length === 0 ? (
              <div className="text-center py-5 text-muted">
                <i className="bi bi-basket3 fs-2 d-block mb-2 text-secondary opacity-75"></i>
                <p className="small mb-1 fw-semibold">No ingredients selected yet</p>
                <p className="small text-muted mb-0">Choose ingredients from the left list to filter dishes</p>
              </div>
            ) : (
              <div className="d-flex flex-wrap gap-1">
                {selected.map((item, idx) => (
                  <span className="badge-ingredient-pill" key={idx}>
                    <span>{item}</span>
                    <button
                      type="button"
                      className="btn-close-pill"
                      onClick={() => handleRemove(item)}
                      aria-label="Remove"
                    >
                      &times;
                    </button>
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      <input type="hidden" name="selected-ingredients" value={selected.join(",")} />

      <div className="d-flex justify-content-end align-items-center gap-3 mt-4 pt-3 border-top">
        <a href="/" className="btn btn-outline-secondary rounded-pill px-4">
          Cancel
        </a>
        <button
          type="submit"
          className="btn-view-recipe px-5 py-2"
          style={{ width: 'auto', minWidth: '220px' }}
          disabled={selected.length === 0}
        >
          <i className="bi bi-search me-1"></i>
          <span>Find Recipes ({selected.length})</span>
        </button>
      </div>
    </div>
  );
}

ReactDOM.render(<AdvancedFilter />, document.querySelector("#advanced-app"));
