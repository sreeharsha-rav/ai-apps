import {
    useLocation,
} from "@remix-run/react";
import { useEffect } from "react";
import { IStaticMethods } from "preline/preline";

// This is a hack to declare the global variable that is used by the preline script.
declare global {
    interface Window {
        HSStaticMethods: IStaticMethods;
    }
}

// This loads the preline script and initializes it.
export default function PrelineScript() {
    const location = useLocation();

    useEffect(() => {
        import("preline/preline");
    }, []);

    useEffect(() => {
        setTimeout(() => {
            window.HSStaticMethods.autoInit();
        }, 100);
    }, [location.pathname]);

    return null;
}