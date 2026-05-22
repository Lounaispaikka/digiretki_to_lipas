# Digiretki — Data Transfer Solution

Point object deduplication pipeline for matching outdoor recreation data with the [lipas.fi](https://lipas.fi/) national database.

**More on the [Digiretki](https://tt.utu.fi/sweng/digiretki/) project [here](https://tt.utu.fi/sweng/digiretki/).**

![](Documentation/banner.png)

## Documentation

- [Lipas synchronization solution](Documentation/lipas_synchronization_solution.md)
- [Deduplication](Documentation/point_deduplication.md)
- [Deduplication pipeline](notebooks/point_deduplicator/README.md)
- [Type mapping (Virma–LIPAS example)](Documentation/virma_lipas_type_mapping/README.md)

## Notebooks

- [`point_deduplicator.ipynb`](notebooks/point_deduplicator/point_deduplicator.ipynb) — match point objects across datasets
- [`route_deduplicator.ipynb`](notebooks/route_deduplication/route_deduplicator.ipynb) — deduplicate route data

Launch with [uv](https://docs.astral.sh/uv/):

```bash
uv run jupyter lab
```

## License

MIT — see [LICENSE](LICENSE.md).

---



Code artifacts produced as part of the [Digiretki](https://tt.utu.fi/sweng/digiretki/) project. Co-funded by the European Union.


<img width="1536" height="343" alt="EU logo" src="https://github.com/user-attachments/assets/9bf00b51-c1d7-4384-8b4b-1d66ff1f88bd" />
