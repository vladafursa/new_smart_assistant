import { NavLink, useLocation, matchPath } from "react-router-dom";
import { FaRegFileAlt, FaHome } from "react-icons/fa";

const Header = () => {
  const location = useLocation();

  // check of path
  const isOnStorage = matchPath("/storage/*", location.pathname);

  // class for icons
  const iconClass = "text-2xl cursor-pointer hover:text-purple-200";

  // render data
  const link = isOnStorage ? "/" : "/storage";
  const Icon = isOnStorage ? FaHome : FaRegFileAlt;
  const aria = isOnStorage ? "Go to home page" : "Go to storage page";

  return (
    <header className="bg-purple-400 text-white px-6 py-3 shadow flex items-center justify-between">
      <h1 className="text-lg font-semibold">Support Assistant</h1>

      <NavLink to={link} end aria-label={aria}>
        <Icon className={iconClass} />
      </NavLink>
    </header>
  );
};

export default Header;
