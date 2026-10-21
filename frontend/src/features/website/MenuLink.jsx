import { Link } from "react-router";

/** One link of an admin-managed menu: {label, url, new_tab}. Site paths use the router. */
export function MenuLink({ link }) {
  if (link.url.startsWith("/") && !link.new_tab) return <Link to={link.url}>{link.label}</Link>;
  return (
    <a href={link.url} {...(link.new_tab && { target: "_blank", rel: "noopener noreferrer" })}>
      {link.label}
    </a>
  );
}
