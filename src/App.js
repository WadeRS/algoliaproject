import React from "react";
import { liteClient as algoliasearch } from "algoliasearch/lite";
import {
  InstantSearch,
  SearchBox,
  Hits,
  RefinementList,
  Pagination,
  Highlight,
  Configure,
} from "react-instantsearch";
import "./styles.css";

const searchClient = algoliasearch(
  "Z1BTQ8RXPW",
  "738ad3170958fa3612990240da3634a6"
);

export default function App() {
  return (
    <InstantSearch searchClient={searchClient} indexName="alpha" insights={true}>
      <Configure hitsPerPage={8} />

      <header className="header">
        <h1 className="header-title">Search Demo</h1>
        <SearchBox
          placeholder="Search for products, brands, or categories"
          className="searchbox"
        />
      </header>

      <main className="container">
        <aside className="sidebar">
          <div className="facet-group">
            <h3>Brands</h3>
            <RefinementList attribute="brand"  />
          </div>

          <div className="facet-group">
            <h3>Categories</h3>
            <RefinementList attribute="hierarchicalCategories.lvl0" />
          </div>
        </aside>

        <section className="results">
          <Hits hitComponent={Hit} />
          <div className="pagination-container">
            <Pagination />
          </div>
        </section>
      </main>
    </InstantSearch>
  );
}

function Hit({ hit, sendEvent }) {
  return (
    <article 
      className="hit-card"
      onClick={() => sendEvent('click', hit, 'Product Clicked')}
    >
      <div className="hit-image-container">
        <img src={hit.image} alt={hit.name} className="hit-image" />
      </div>
      <div className="hit-info">
        <p className="hit-category">{hit.categories[0]}</p>
        <h2 className="hit-name">
          <Highlight attribute="name" hit={hit.name} />
        </h2>
        <p className="hit-price">${hit.price}</p>
      </div>
    </article>
  );
}