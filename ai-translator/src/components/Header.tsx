import * as SubframeCore from "@subframe/core";

/**
 * Renders the header component for the AI Translator application.
 *
 * @returns {JSX.Element} The header component.
 */
const Header: React.FC = () => {
    return (
        <div className="flex w-full max-w-[576px] items-center gap-4">
        <div className="flex grow shrink-0 basis-0 items-center gap-2">
          <SubframeCore.Icon
            className="text-heading-2 font-heading-2 text-default-font"
            name="FeatherMessageCircle"
          />
          <span className="text-heading-3 font-heading-3 text-default-font text-xl">
            AI Translator
          </span>
        </div>
      </div>
    );
};

export default Header;