function ShowSelected() {
  const [selected, setSelected] = React.useState([]);
  const ingredients = Array.from(document.querySelector("#ingredient").options);

  function Add() {

    const handleAdd = (event) =>{
        const value = event.target.value;
        if (value && !selected.includes(value)) {
        setSelected(prevSelected => [...prevSelected, value]);
        }
    }

    return (
      <select className="form-select" id="ingredient" name="ingredient" multiple size="20">
        {ingredients.map(ingredient => (
          <option value={ingredient.value} onDoubleClick={handleAdd}>
            {ingredient.text}
          </option>
        ))}
      </select>
    )
  }
  
  ReactDOM.render(
    <Add />,
    document.querySelector("#ingredient-list")
  );
  
  return (
    <div>
      {selected.map(ingredient => (
        <span className="badge bg-warning text-dark m-2">{ingredient}
          <button type="button" className="btn-close m-1"
            onClick={() => setSelected(selected.filter(item => item !== ingredient))}>
          </button>
        </span>
        ))}
        <input type="hidden" name="selected-ingredients" value={selected.join(",")} />
      </div>
  );
}

ReactDOM.render(
  <ShowSelected />,
  document.querySelector("#selected-ingredients-container")
);
