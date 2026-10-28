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
        if (!data.recipes || data.recipes.length === 0) {
          setHasMore(false);
        } else {
          setRecipes(prev => {
            const existingIds = new Set(prev.map(r => r.id));
            const newRecipes = data.recipes.filter(r => !existingIds.has(r.id));
            return [...prev, ...newRecipes];
          });
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
        window.innerHeight + window.scrollY >= document.body.offsetHeight - 350 &&
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
    <div>
      <div className="catalog-header">
        <div>
          <h2 className="catalog-title">Explore Recipes</h2>
          <p className="text-muted small mb-0">Handpicked collection of mouthwatering meals</p>
        </div>
        <div className="text-muted small fw-semibold">
          <i className="bi bi-grid-fill me-1" style={{ color: 'var(--primary)' }}></i>
          Showing {recipes.length} dishes
        </div>
      </div>

      <div className="row g-4">
        {recipes.map(recipe => (
          <div className="col-xl-3 col-lg-4 col-md-6 col-sm-12" key={recipe.id}>
            <div className="recipe-card">
              <div className="recipe-card-img-wrapper">
                <img
                  src={recipe.image_url || 'https://images.unsplash.com/photo-1495521821757-a1efb6729352?w=600&auto=format&fit=crop&q=80'}
                  className="recipe-card-img"
                  alt={recipe.title}
                  loading="lazy"
                  onError={(e) => {
                    e.target.onerror = null;
                    e.target.src = 'https://images.unsplash.com/photo-1495521821757-a1efb6729352?w=600&auto=format&fit=crop&q=80';
                  }}
                />
              </div>
              <div className="recipe-card-body">
                <h5 className="recipe-card-title" title={recipe.title}>{recipe.title}</h5>
                <a href={`/recipe/${recipe.id}`} className="btn-view-recipe">
                  <span>View Recipe</span>
                  <i className="bi bi-arrow-right"></i>
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>

      {loading && (
        <div className="d-flex flex-column align-items-center justify-content-center py-5 my-4">
          <div className="spinner-border spinner-custom mb-3" role="status">
            <span className="visually-hidden">Loading recipes...</span>
          </div>
          <span className="text-muted small fw-semibold">Loading more delicious recipes...</span>
        </div>
      )}

      {!hasMore && (
        <div className="text-center py-5 my-3 text-muted">
          <i className="bi bi-check-circle-fill me-2 fs-5" style={{ color: 'var(--primary)' }}></i>
          <span className="fw-semibold">You've reached the end of the collection!</span>
        </div>
      )}
    </div>
  );
}

ReactDOM.render(<Catalog />, document.querySelector("#catalog"));
