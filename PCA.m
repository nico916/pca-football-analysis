% Étape 1 : Chargement des données et préparation
data = readtable('player_stats_processed.csv', 'Delimiter', ';', 'VariableNamingRule', 'preserve');
player_names = data.Player;

% Étape 2 : Recatégorisation des postes en FW, MF, DF
original_positions = data.Pos;
new_positions = cell(size(original_positions));
for i = 1:length(original_positions)
    pos_str = lower(original_positions{i});
    if strncmpi(pos_str, 'fw', 2)
        new_positions{i} = 'FW';
    elseif strncmpi(pos_str, 'mf', 2)
        new_positions{i} = 'MF';
    elseif strncmpi(pos_str, 'df', 2)
        new_positions{i} = 'DF';
    else
        new_positions{i} = 'DF';
    end
end
data.Pos = new_positions;

% Étape 3 : Extraction des variables numériques
data_numeric = data{:, varfun(@isnumeric, data, 'OutputFormat', 'uniform')};
var_names = data.Properties.VariableNames(varfun(@isnumeric, data, 'OutputFormat', 'uniform'));

% Étape 4 : Standardisation
data_mean = mean(data_numeric, 1);
data_std = std(data_numeric, 0, 1);
data_standardized = (data_numeric - data_mean) ./ data_std;

% Étape 5 : PCA
cov_matrix = cov(data_standardized);
[eigenvectors, eigenvalues_matrix] = eig(cov_matrix);
eigenvalues = diag(eigenvalues_matrix);
[eigenvalues_sorted, idx] = sort(eigenvalues, 'descend');
eigenvectors_sorted = eigenvectors(:, idx);
pca_scores = data_standardized * eigenvectors_sorted;

% Étape 6 : Analyse des corrélations entre variables
corr_matrix = corr(data_standardized);
n_vars = size(corr_matrix,1);
corr_vals = [];
pairs = {};
for r = 1:n_vars-1
    for c = r+1:n_vars
        corr_vals(end+1) = corr_matrix(r,c);
        pairs{end+1} = {var_names{r}, var_names{c}};
    end
end
[sorted_corr, sorted_idx] = sort(abs(corr_vals), 'descend');
sorted_pairs = pairs(sorted_idx);
sorted_corr_actual = corr_vals(sorted_idx);

disp('Les 5 paires de variables les plus corrélées :');
for i = 1:min(5, length(sorted_corr))
    fprintf('%s et %s : Corr = %.2f\n', sorted_pairs{i}{1}, sorted_pairs{i}{2}, sorted_corr_actual(i));
end

disp('Les 5 paires de variables les moins corrélées :');
for i = max(length(sorted_corr)-4,1):length(sorted_corr)
    fprintf('%s et %s : Corr = %.2f\n', sorted_pairs{i}{1}, sorted_pairs{i}{2}, sorted_corr_actual(i));
end

% Étape 7 : Affichage graphique PCA
fig = figure('Color','w');
hold on;
pos_categories_ordered = {'FW', 'MF', 'DF'};
category_colors = [0.984, 0.6, 0.6; 0.6, 0.8, 0.98; 0.6, 0.9, 0.6]; 
h = gobjects(length(pos_categories_ordered), 1);
global_indices = [];
for i = 1:length(pos_categories_ordered)
    pos_category = pos_categories_ordered{i};
    idx_cat = strcmp(data.Pos, pos_category);
    h(i) = scatter(pca_scores(idx_cat, 1), pca_scores(idx_cat, 2), 60, category_colors(i, :), 'filled', ...
        'MarkerEdgeColor',[0.3 0.3 0.3], 'MarkerFaceAlpha',0.8);
    global_indices = [global_indices; find(idx_cat)];
end
xline(0, '--', 'LineWidth', 1, 'Color', [0.5 0.5 0.5]); 
yline(0, '--', 'LineWidth', 1, 'Color', [0.5 0.5 0.5]); 

var_contributions = sqrt(sum(eigenvectors_sorted(:,1:2).^2,2));
max_contribution = max(var_contributions);
scaling_factor = 5; 
for i = 1:size(eigenvectors_sorted, 1)
    arrow_length = scaling_factor * (var_contributions(i) / max_contribution);
    quiver(0, 0, arrow_length * eigenvectors_sorted(i, 1), arrow_length * eigenvectors_sorted(i, 2), ...
        'MaxHeadSize', 0.5, 'LineWidth', 1.5, 'Color', [0.4 0 0.4 0.7]);
    text(arrow_length * eigenvectors_sorted(i, 1)*1.1, arrow_length * eigenvectors_sorted(i, 2)*1.1, ...
        var_names{i}, 'FontSize', 10, 'Color', [0.3 0 0.3], 'FontName','Helvetica');
end
grid on;
set(gca, 'GridColor', [0.9 0.9 0.9], 'MinorGridColor', [0.95 0.95 0.95]);
set(gca, 'FontName','Helvetica', 'FontSize',12);
box on;

pc1_var = (eigenvalues_sorted(1)/sum(eigenvalues))*100;
pc2_var = (eigenvalues_sorted(2)/sum(eigenvalues))*100;
xlabel(sprintf('Première Composante Principale (%.2f%%)', pc1_var), 'FontWeight','bold', 'FontSize',14);
ylabel(sprintf('Deuxième Composante Principale (%.2f%%)', pc2_var), 'FontWeight','bold', 'FontSize',14);
title('Projection PCA avec Contributions des Variables et Axes Conceptuels', 'FontSize',16, 'FontWeight','bold');

legend(h, pos_categories_ordered, 'Location', 'best', 'FontSize',12, 'FontName','Helvetica');

text(max(pca_scores(:, 1)) * 1.1, 0, 'Offensif', 'FontSize', 14, 'FontWeight', 'bold', 'HorizontalAlignment', 'center', 'Color', [0.8 0.2 0.2]);
text(min(pca_scores(:, 1)) * 1.1, 0, 'Défensif', 'FontSize', 14, 'FontWeight', 'bold', 'HorizontalAlignment', 'center', 'Color', [0.2 0.2 0.8]);
text(0, max(pca_scores(:, 2)) * 1.1, 'Créatif', 'FontSize', 14, 'FontWeight', 'bold', 'HorizontalAlignment', 'center', 'Color', [0.3 0.3 0.3]);
text(0, min(pca_scores(:, 2)) * 1.1, 'Stéréotypé', 'FontSize', 14, 'FontWeight', 'bold', 'HorizontalAlignment', 'center', 'Color', [0.3 0.3 0.3]);

text(max(pca_scores(:, 1)) * 0.75, max(pca_scores(:, 2)) * 0.75, ...
    'Créateurs Offensifs', 'FontSize', 12, 'FontWeight', 'bold', 'HorizontalAlignment', 'center', 'Color', [0.9 0.4 0.4]);
text(min(pca_scores(:, 1)) * 0.75, max(pca_scores(:, 2)) * 0.75, ...
    'Créateurs Défensifs', 'FontSize', 12, 'FontWeight', 'bold', 'HorizontalAlignment', 'center', 'Color', [0.4 0.4 0.9]);
text(min(pca_scores(:, 1)) * 0.75, min(pca_scores(:, 2)) * 0.75, ...
    'Rugueux Défensifs', 'FontSize', 12, 'FontWeight', 'bold', 'HorizontalAlignment', 'center', 'Color', [0.4 0.7 0.4]);
text(max(pca_scores(:, 1)) * 0.75, min(pca_scores(:, 2)) * 0.75, ...
    'Finisseurs', 'FontSize', 12, 'FontWeight', 'bold', 'HorizontalAlignment', 'center', 'Color', [0.8 0.4 0.8]);

dcm_obj = datacursormode(fig);
set(dcm_obj, 'UpdateFcn', @(src, event) displayPlayerName(event, player_names, pca_scores, global_indices));

c = uicontextmenu;
fig.UIContextMenu = c;
uimenu(c,'Label','Afficher FW uniquement','Callback',@(src,event)filterByCategory(fig, pca_scores, data, global_indices, 'FW', player_names));
uimenu(c,'Label','Afficher MF uniquement','Callback',@(src,event)filterByCategory(fig, pca_scores, data, global_indices, 'MF', player_names));
uimenu(c,'Label','Afficher DF uniquement','Callback',@(src,event)filterByCategory(fig, pca_scores, data, global_indices, 'DF', player_names));
uimenu(c,'Label','Afficher tous','Callback',@(src,event)filterByCategory(fig, pca_scores, data, global_indices, 'ALL', player_names));

function output_txt = displayPlayerName(event, player_names, pca_scores, global_indices)
    pos = event.Position;
    idx_scatter = find(pca_scores(global_indices, 1) == pos(1) & pca_scores(global_indices, 2) == pos(2), 1);
    if ~isempty(idx_scatter)
        idx_global = global_indices(idx_scatter);
        output_txt = sprintf('Nom: %s', player_names{idx_global});
    else
        output_txt = 'Point non associé';
    end
end

function filterByCategory(fig, pca_scores, data, global_indices, category, player_names)
    axes_handle = findobj(fig,'Type','axes');
    ax = axes_handle(1);
    hold(ax,'on')
    delete(findobj(ax,'Type','Scatter'));
    if strcmp(category,'ALL')
        idx_show = true(size(data.Pos));
    else
        idx_show = strcmp(data.Pos, category);
    end
    pos_categories_ordered = {'FW', 'MF', 'DF'};
    colors = [0.984, 0.6, 0.6; 0.6, 0.8, 0.98; 0.6, 0.9, 0.6];
    h = gobjects(length(pos_categories_ordered),1);
    global_indices_new = [];
    for i = 1:length(pos_categories_ordered)
        idx_cat = strcmp(data.Pos, pos_categories_ordered{i}) & idx_show;
        h(i) = scatter(pca_scores(idx_cat,1), pca_scores(idx_cat,2),50,colors(i,:),'filled','Parent',ax,'MarkerFaceAlpha',0.8,'MarkerEdgeColor',[0.3 0.3 0.3]);
        global_indices_new = [global_indices_new; find(idx_cat)];
    end
    legend(h,pos_categories_ordered,'Location','best');
    dcm_obj = datacursormode(fig);
    set(dcm_obj,'UpdateFcn',@(src,event)displayPlayerName(event,player_names,pca_scores,global_indices_new));
    hold(ax,'off')
end
