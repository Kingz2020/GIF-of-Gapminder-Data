import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import imageio
sns.set()

path = 'data/'


def prepare_fertility():
    '''   '''
    fert = pd.read_csv(path+'gapminder_total_fertility.csv', index_col=0)
    fert.index.name = 'country'
    fert.columns = fert.columns.astype(int)
    fert = fert.reset_index()
    fert = fert.melt(id_vars='country', var_name='year',
                     value_name='fertility_rate')
    return fert


def prepare_population():
    '''   '''
    population = pd.read_excel(path +
                               'gapminder_population.xlsx', index_col=0)
    population.index.name = 'country'
    population = population.reset_index()
    population = population.melt(
        id_vars='country', var_name='year', value_name='population')
    return population


def prepare_life():
    ''''''
    life = pd.read_excel(path+'gapminder_lifeexpectancy.xlsx', index_col=0)
    life.index.name = 'country'
    life = life.reset_index()
    life = life.melt(id_vars='country', var_name='year',
                     value_name='life_expectancy')
    return life


def prepare_mortality():
    ''''''
    child_mort = pd.read_csv(path +
                             'child_mortality_0_5_year_olds_dying_per_1000_born.csv',
                             index_col=0)
    child_mort.index.name = 'country'
    child_mort.columns = child_mort.columns.astype(int)
    child_mort = child_mort.reset_index()
    child_mort = child_mort.melt(
        id_vars='country', var_name='year', value_name='child_mortality')
    return child_mort


def store_pics():
    for i in range(1960, 2016):
        fig = plt.figure(1)
        fig.clf()
        ax = plt.subplot(111)
        ax.set_xlim(0.4, 1.3)
        ax.set_ylim(0, 10)
        df_pic = df_clean[df_clean['year'] == i]
        plt.gcf().set_size_inches((20, 20))
        sns.set_style('whitegrid')
        plt.title('The Change')
        plt.style.use('fivethirtyeight')
        sns.scatterplot(x='child_mort_%', y='fertility_rate', hue='continent',
                        data=df_pic, size='population', sizes=(50, 3200),
                        alpha=0.6, ax=ax, legend='brief')
        plt.xlabel('% Child Survival')
        plt.ylabel('Children per Woman')
        ax.text(0.25, 0.38, i, size=250, alpha=0.1, transform=ax.transAxes)
        plt.savefig(path + 'pics/lifeexp_{}.png'.format(i))
    return print('pics created and stored')


def create_gif():
    images = []
    a = 1960
    b = 2016

    for i in range(a, b):
        filename = path + 'pics/lifeexp_{}.png'.format(i)
        images.append(imageio.imread(filename))
    imageio.mimsave('output.gif', images, fps=20)
    return print('gif created')


fert = prepare_fertility()
population = prepare_population()

df = fert.merge(population)
life = prepare_life()
df = df.merge(life)

df_subset = df.loc[df['country'].isin(['France', 'Germany', 'Sweden'])]
continent = pd.read_csv(path + 'continents.csv', sep=';')
df_clean = df.dropna()
df_clean = df_clean.merge(continent)
child_mort = prepare_mortality()
df_clean = df_clean.merge(child_mort)

df_clean['child_mort_%'] = df_clean['child_mortality'].transform(
    lambda x: 1 - x/100)
store_pics()
create_gif()
