def age_split(data_series, split_point, value="MgCa"):
    # Split the dataframe into two parts
    before = data_series[data_series.age_ka > split_point]
    after = data_series[data_series.age_ka < split_point]
    # Return the means
    return after[value].mean(), after[value].std(), before[value].mean(), before[value].std()


def plot_split(ax, data_series, split_point, value):
    after_mean, after_error, before_mean, before_error = age_split(data_series, split_point, value)
    ax.plot([data_series.age_ka.min(), split_point], [after_mean, after_mean],
                   label=f'Post-{split_point} kyr = {after_mean:.2} ± {after_error:.1}', color='tab:blue')
    ax.fill_between([data_series.age_ka.min(), split_point], [after_mean - after_error, after_mean - after_error],
        [after_mean + after_error, after_mean + after_error], alpha=0.1, color="tab:blue", ec=None)
    ax.plot([split_point, data_series.age_ka.max()],[before_mean, before_mean],
                   label=f'Pre-{split_point} kyr = {before_mean:.2} ± {before_error:.1}', color="tab:red")
    ax.fill_between([split_point, data_series.age_ka.max()], [before_mean - before_error, before_mean - before_error],
        [before_mean + before_error, before_mean + before_error], alpha=0.1, color="tab:red", ec=None)
    print(f'Post-{split_point} kyr = {after_mean:.2} ± {after_error:.1}')
    print(f'Pre-{split_point} kyr = {before_mean:.2} ± {before_error:.1}')
    print(f'Difference in {value} over {split_point} = {(after_mean - before_mean):.2} ± {(after_error + before_error):.2}')
    return ax


if __name__ == "__main__":
    pass
