# from selenium.common.exceptions import ElementClickInterceptedException
# from seleniumbase import SB


# def search_slot(timeout: int = 10) -> str:
#     url = (
#         "https://www.phorest.com/salon/moranterue1"
#         "/book/service-selection?showSpecialOffers=false"
#     )

#     with SB(browser="chrome", headless=True) as sb:
#         sb.open(url)
#         sb.click_if_visible(
#             "#onetrust-accept-btn-handler, #onetrust-close-btn-container",
#             timeout=timeout,
#         )
#         steps = [
#             "//button[@data-testid='serviceCategory' and .//div[contains(.,'Herren Schneiden')]]",
#             "//div[@data-testid='serviceItem' and .//div[contains(.,'Schnitt - Herren')]]",
#             "//div[@data-testid='staffMembersTab' and .//div[normalize-space()='Team']]",
#             "//div[starts-with(@data-testid,'staffMemberButton_') and .//div[contains(.,'Leandro')]]",
#             "//button[@data-testid='bookButton']",
#         ]
#         for xpath in steps:
#             sb.wait_for_element_visible(xpath, by="xpath", timeout=timeout)
#             el = sb.find_element(xpath, by="xpath")
#             sb.execute_script(
#                 "arguments[0].scrollIntoView({block:'center', inline:'nearest'});", el
#             )
#             sb.wait_for_ready_state_complete()
#             sb.sleep(0.15)  # necessary
#             sb.wait_for_element_clickable(xpath, by="xpath", timeout=timeout)

#             # Try regular click first; fall back to JS if something still intercepts
#             try:
#                 sb.click(xpath, by="xpath")
#             except ElementClickInterceptedException:
#                 sb.js_click(xpath, by="xpath")

#         target = "//div[@data-testid='availabilityAgenda']"
#         sb.wait_for_element_visible(target, by="xpath", timeout=timeout)
#         inner_html = sb.get_attribute(target, "innerHTML", by="xpath")
#         if not inner_html:
#             raise LookupError("availabilityAgenda was empty.")
#         return str(inner_html)
