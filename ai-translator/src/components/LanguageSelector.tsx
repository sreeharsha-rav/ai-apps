// Presentational component that displays a list of languages to select from.

import Image from "next/image";

/**
 * Tailwind CSS styles for the LanguageSelector component.
 */
const styles = {
    langSelect_wrapper: "flex max-h-[48px] w-full grow shrink-0 basis-0 flex-wrap items-start gap-12 pr-6 pl-6",
    lang_wrapper: "flex max-h-[48px] grow shrink-0 basis-0 items-center justify-center gap-4 self-stretch overflow-hidden rounded border border-solid border-neutral-border pt-4 pr-4 pb-4 pl-4 bg-white hover:shadow transition-shadow duration-300 ease-in-out cursor-pointer",
    lang_active: "opacity-100 bg-neutral-100 rounded",
    lang_passive: "opacity-50 hover:opacity-100 transition-opacity duration-300 ease-in-out",
    lang_img_container: "flex h-8 w-8 flex-none flex-col items-start overflow-hidden rounded border border-solid border-neutral-border bg-default-background",
    lang_img: "w-full grow shrink-0 basis-0 object-cover",
    lang_text_container: "flex grow shrink-0 basis-0 flex-col items-start justify-center gap-1",
    lang_text: "text-heading-3 font-heading-3 text-default-font"
};

/**
 * Languages for the LanguageSelector component.
 */
const flags = [
    {
        "language": "French",
        "url": "https://flagcdn.com/w80/fr.png"
    },
    {
        "language": "Spanish",
        "url": "https://flagcdn.com/w80/es.png"
    },
    {
        "language": "Japanese",
        "url": "https://flagcdn.com/w80/jp.png"
    }
]

/**
 * Props for the Language component.
 * 
 * @interface LanguageProps
 * @property {string} language - The language.
 * @property {string} imageUrl - The image URL for the language.
 */
interface LanguageProps {
    language: string;
    imageUrl: string;
}

/**
 * Represents the Language component.
 * 
 * @param {LanguageProps} props - The props for the Language component.
 * @returns {JSX.Element} The Language component.
 */
const Language: React.FC<LanguageProps> = ({ language, imageUrl })  => {
    return (
        <div className={styles.lang_wrapper}>
              <div className={styles.lang_img_container}>
                <Image
                  className={styles.lang_img}
                  src={imageUrl}
                  alt={language}
                  width={80}
                  height={80}
                />
              </div>
              <div className={styles.lang_text_container}>
                <span className={styles.lang_text}>
                  {language}
                </span>
              </div>
        </div>
    );
}

/**
 * Props for the LanguageSelector component.
 * 
 * @interface LanguageSelectorProps
 * @property {string} selectedLanguage - The selected language.
 * @property {Function} onLanguageChange - The function to handle language change.
 */
interface LanguageSelectorProps {
    selectedLanguage: string;
    onLanguageChange: (language: string) => void;
}

/**
 * Represents the LanguageSelector component.
 * 
 * @returns {JSX.Element} The LanguageSelector component.
 */
const LanguageSelector: React.FC<LanguageSelectorProps> = ({ selectedLanguage, onLanguageChange }) => {
    return (
        <div className={styles.langSelect_wrapper}>
            {flags.map((flag) => (
                <div
                    key={flag.language}
                    onClick={() => onLanguageChange(flag.language)}
                    className={`${selectedLanguage === flag.language ? styles.lang_active : styles.lang_passive}`}
                >
                    <Language key={flag.language} language={flag.language} imageUrl={flag.url} />
                </div>
            ))}
        </div>
    );
};

export default LanguageSelector;