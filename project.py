from logger import get_logger, set_all_loggers_debug
from otm_helper import OnTheMarketSearch
from beautifultable import BeautifulTable
import argparse


LOG_LEVEL = "INFO"
PROGRAM_NAME = "Property finder"
logger = get_logger(PROGRAM_NAME)


def main():
    params = get_args()
    keywords = [x.strip() for x in params.keywords.split(",")] if params.keywords else []
    logger.debug(f"Keywords are: {keywords}")
    otm_search = OnTheMarketSearch(postcode=params.postcode, radius=params.radius,
                                   min_price=params.min_price, max_price=params.max_price,
                                   min_bed=params.min_bed, max_bed=params.max_bed,
                                   property_type=params.type, potential=params.potential, keywords=keywords)
    logger.info(f"Results: \n" + \
                f"{display_search_results(otm_search)} \n" + \
                "\n" + \
                f"Area stats ({otm_search.radius} miles around {otm_search.postcode.upper()}): \n" + \
                f"{display_stats_for_area(otm_search)}")


def display_search_results(otm_search):
    avg_price_per_sqm = otm_search.average_price_per_sqm["price"]
    table = BeautifulTable(maxwidth=500)
    table.columns.header = ["Postcode", "Price", "£/m2", "Benchmark", "Stamp duty", "Beds",
                            "Surface", "Type", "Days since", "Desc", "URL", "Potential", "Keywords found"]
    for property in sorted(otm_search.results, key = lambda x: (OnTheMarketSearch.detailed_to_general_property_type_map.get(x.property_type, "Other"), x.price_per_sqm)):
        market_benchmark = int((property.price_per_sqm / avg_price_per_sqm - 1)
                               * 100 if (property.price_per_sqm > 0 and avg_price_per_sqm > 0) else 0)
        if market_benchmark > 100:
            logger.error(f"Skipping property {
                         property.url} which has a crazy price per sqm (most likely due to incorrect surface)")
            continue
        table.rows.append([property.postcode, f"£{property.price:,}", f"£{property.price_per_sqm:,}" if property.price_per_sqm > 0 else "-",
                           f"{market_benchmark:,}%" if property.price_per_sqm > 0 else "-", f"£{property.stamp_duty:,}",
                           property.bedrooms, f"{
                               property.sqm_surface_area} m2" if property.sqm_surface_area > 0 else "-", property.property_type,
                           property.days_since_added_or_reduced, property.short_description, property.url, "Y" if property.has_potential else "-",
                           ", ".join(property.keywords_found)])

    to_display = "Results\n"
    to_display += f"{table}\n"
    to_display += f"{len(otm_search.results)} results found - Average £/m2: {avg_price_per_sqm:,}"
    return to_display


def display_stats_for_area(otm_search):
    table = BeautifulTable(maxwidth=500)
    table.columns.header = ["Property type", "Average £/m2", "# of properties in sample"]
    for property_type, avg_price_data in otm_search.average_price_per_sqm_per_type.items():
        table.rows.append([property_type, f"£{avg_price_data["price"]:,}", avg_price_data["sample_size"]])
    return table


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--postcode", help="Postcode for the search", type=str, required=True)
    parser.add_argument("--radius", help="Radius for the search", type=float, required=True)
    parser.add_argument("--min-price", help="Minimum price ", type=int, required=False)
    parser.add_argument("--max-price", help="Maximum price", type=int, required=False)
    parser.add_argument("--min-bed", help="Minimum number of bedrooms", type=int, required=False)
    parser.add_argument("--max-bed", help="Maximum number of bedrooms", type=int, required=False)
    parser.add_argument(
        "--type", help="Type of property: case be 'house', 'flat' or nothing for all types", choices = ["house", "flat"], type=str, required=False)
    parser.add_argument("--potential", action='store_true')
    parser.add_argument(
        "--keywords", help="Additional criteria (garden, STPP, fireplace, ...)", type=str, required=False)
    parser.add_argument("--debug", action='store_true')
    args = parser.parse_args()
    if args.debug:
        set_all_loggers_debug(True)

    clean_postcode = args.postcode.lower().replace(" ", "")
    clean_postcode = clean_postcode[:-3] + "-" + clean_postcode[-3:]
    args.postcode = clean_postcode

    args.radius = float(int(args.radius * 4)) / 4   # OnTheMarket only allows multiples of 0.25
    if args.radius < 0.25:
        args.radius = 0.25

    return args


if __name__ == "__main__":
    main()
