interface ArticleConfigTemplateProps {
    newspaperid: number;
    fullView?: boolean;
}

const ArticleConfigTemplate: React.FC<ArticleConfigTemplateProps> = ({ newspaperid, fullView = false }) => {
    return (
        <div>
            <h1>My Article Content Configuration {newspaperid}</h1>
        </div>
    );
};

export default ArticleConfigTemplate;
