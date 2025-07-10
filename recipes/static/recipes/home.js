function Catalog() {
  const [recipes, setRecipes] = React.useState([]);
  const [loading, setLoading] = React.useState(true);
  const [page, setPage] = React.useState(1);
  const [hasMore, setHasMore] = React.useState(true);

  React.useEffect(() => {
    setLoading(true);
    fetch(`/load_recipe_cards?page=${page}`)
      .then(response => response.json())
      .then(data => {
        if (data.recipes.length === 0) {
          setHasMore(false);
        } else {
          setRecipes(prev => [...prev, ...data.recipes]);
        }
        setLoading(false);
      })
      .catch(error => {
        setLoading(false);
        setHasMore(false);
        console.error('Error fetching recipes:', error);
      });
  }, [page]);

  React.useEffect(() => {
    function handleScroll() {
      if (
        window.innerHeight + window.scrollY >= document.body.offsetHeight - 200 &&
        !loading &&
        hasMore
      ) {
        setPage(prev => prev + 1);
      }
    }
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [loading, hasMore]);

  return (
    <div className="row justify-content-center mx-4">
      <h1 className="text-center text-primary-emphasis my-3">Browse Recipes</h1>
      {recipes.map(recipe => (
        <div className="card my-3 mx-4 col-md-3 col-lg-2 col-sm-6 bg-warning-subtle" key={recipe.id}>
          <img src={recipe.image_url} className="card-img-top img-fluid mt-3" alt={recipe.title} />
          <div className="card-body">
            <h5 className="card-title">{recipe.title}</h5>
            <a href={`/recipe/${recipe.id}`} className="btn btn-outline-primary">View Recipe</a>
          </div>
        </div>
      ))}
      {loading && <div className="text-center">Loading...</div>}
      {!hasMore && <div className="text-center text-muted mb-3">No more recipes.</div>}
    </div>
  );
}

ReactDOM.render(<Catalog />, document.querySelector("#catalog"));
