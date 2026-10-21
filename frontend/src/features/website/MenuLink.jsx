import { Link } from "react-router";

/**
 * One link of an admin-managed menu: {label, url, new_tab}. Site paths use the
 * router. `children` replaces the label as the content (for richer rows).
 */
export function MenuLink({ link, children, ...rest }) {
  const content = children ?? link.label;
  if (link.url.startsWith("/") && !link.new_tab) {
    return <Link to={link.url} {...rest}>{content}</Link>;
  }
  return (
    <a href={link.url} {...rest} {...(link.new_tab && { target: "_blank", rel: "noopener noreferrer" })}>
      {content}
    </a>
  );
}
